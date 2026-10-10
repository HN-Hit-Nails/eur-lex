#!/usr/bin/env python3
"""Colecções do Cellar além da legislação em vigor (ue/): jurisprudência, orientações da Comissão
publicadas no JO C, legislação que já não está em vigor e propostas da Comissão.

Comandos (por colecção):
  listas <colecção>        lista de trabalho (.cache/arquivo/<colecção>/lista.json), do SPARQL do Cellar
  descarregar <colecção>   obtém o texto em português (em paralelo; retoma onde parou)
  converter <colecção>     escreve os ficheiros Markdown e o INDICE.tsv da colecção
  tudo <colecção>          os três passos

Colecções:
  jurisprudencia-curada  acórdãos, despachos e conclusões citados nos .contexto.md do corpus curado
                         -> jurisprudencia/<ano>/<CELEX>.md (neste repositório)
  orientacoes            comunicações, orientações e guias da Comissão publicados no JO C
                         -> orientacoes/comissao/<ano>/<CELEX>.md (neste repositório)
  jurisprudencia         toda a jurisprudência com texto em português (Tribunal de Justiça, Tribunal
                         Geral, Tribunal da Função Pública; acórdãos, despachos, conclusões, pareceres)
  revogada               legislação que o Cellar marca como não estando em vigor
  propostas              propostas legislativas da Comissão (COM)

As três últimas são grandes (≈0,5 a 2 GB de texto cada) e vão para outro repositório: indicar a
pasta da cópia local com --raiz (ex.: --raiz ../eur-lex-arquivo).

Só se descarrega texto em português; os documentos sem texto em português ficam de fora (os que
não estão na lista são contados no INDICE.md da colecção). Texto descarregado guardado comprimido
em .cache/arquivo/ (fora do git), para poder reconverter.
"""

import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import gzip
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import eurlex  # noqa: E402
import completo  # noqa: E402

RAIZ = eurlex.RAIZ
CACHE = RAIZ / ".cache" / "arquivo"
POR = "<http://publications.europa.eu/resource/authority/language/POR>"

TIPOS_JURIS = {"CJ": "Acórdão do Tribunal de Justiça", "CC": "Conclusões do advogado-geral",
               "CO": "Despacho do Tribunal de Justiça", "CV": "Parecer do Tribunal de Justiça",
               "CP": "Tomada de posição do advogado-geral", "TJ": "Acórdão do Tribunal Geral",
               "TO": "Despacho do Tribunal Geral", "FJ": "Acórdão do Tribunal da Função Pública",
               "FO": "Despacho do Tribunal da Função Pública"}
# Comunicações da Comissão no JO C que explicam como aplicar o direito (orientações, guias,
# enquadramentos, perguntas e respostas), sem os avisos de casos concretos e listas periódicas.
RE_ORIENTACOES = (r"^(comunica[çc][ãa]o da comiss[ãa]o|orienta[çc][õo]es|enquadramento|quadro tempor[áa]rio|guia)"
                  r"|orienta[çc][õo]es|\bguia\b|perguntas e respostas|nota interpretativa")
EXCLUIR_ORIENTACOES = (r"^(informa[çc][õo]es (sint[ée]ticas )?(comunicadas|transmitidas)|aux[íi]lios? estata(l|is) ?[—-]"
                       r"|convite|.*lista de organismos)|taxas? de (juro|c[âa]mbio|refer[êe]ncia)|concentra[çc][ãa]o"
                       r"|n[ãa]o aplica[çc][ãa]o de determinadas")


def destino_base(col, raiz):
    return {"jurisprudencia-curada": raiz / "jurisprudencia", "jurisprudencia": raiz / "jurisprudencia",
            "orientacoes": raiz / "orientacoes" / "comissao", "revogada": raiz / "ue-revogada",
            "propostas": raiz / "propostas"}[col]


def pasta(col, celex):
    if col == "revogada":
        return completo.pasta(celex)
    return celex[1:5]


def ficheiro(col, raiz, celex):
    return destino_base(col, raiz) / pasta(col, celex) / f"{completo.nome_ficheiro(celex)}.md"


# ---------------------------------------------------------------------------
# Listas
# ---------------------------------------------------------------------------

def por_tipo(sector, tipos, corpo, campos, anos=None):
    """Consulta por tipo de documento e por ano, com o tipo e o ano como literais exactos: o Cellar
    responde em segundos (filtrar pelo texto do CELEX percorre tudo e demora minutos; sem dividir por
    ano, as consultas com FILTER EXISTS falham com erro 500)."""
    linhas = []
    for tp in tipos:
        for ano in anos or ANOS:
            filtro_ano = f'; cdm:resource_legal_year "{ano}"^^xsd:gYear'
            q = eurlex.PREFIXOS + f"""SELECT ?celex {campos} WHERE {{
  ?w cdm:resource_legal_id_sector "{sector}"^^xsd:string ; cdm:resource_legal_type "{tp}"^^xsd:string {filtro_ano} ;
     cdm:resource_legal_id_celex ?celex .
  {corpo}
}} GROUP BY ?celex ORDER BY ?celex"""
            linhas += completo._paginar(q)
    return linhas


def por_celex(celexes, corpo, campos, lote=80):
    linhas = []
    for i in range(0, len(celexes), lote):
        valores = " ".join(eurlex._lit(c) for c in celexes[i:i + lote])
        linhas += eurlex.sparql(eurlex.PREFIXOS + f"""SELECT ?celex {campos} WHERE {{
  VALUES ?celex {{ {valores} }}
  ?w cdm:resource_legal_id_celex ?celex .
  {corpo}
}} GROUP BY ?celex""")
    return linhas


ANOS = list(range(1951, dt.date.today().year + 2))
TIPOS_3 = list("RLDHMJABOEFGCKQSXY")


def titulo_pt(obrigatorio=True):
    t = f"""?e cdm:expression_belongs_to_work ?w ; cdm:expression_uses_language {POR} ; cdm:expression_title ?t .
  FILTER EXISTS {{ ?m cdm:manifestation_manifests_expression ?e }}"""
    return t if obrigatorio else "OPTIONAL { " + t + " }"


def citados_no_corpus():
    res = set()
    for f in eurlex.CORPUS.glob("*/*.contexto.md"):
        res |= set(re.findall(r"\b6\d{4}(?:CJ|TJ|CC|CO|TO|CV|CP|FJ|FO)\d{4}(?:\(\d{2}\))?",
                              f.read_text(encoding="utf-8")))
    return res


def cmd_listas(col):
    hoje = dt.date.today().isoformat()
    actos = {}
    if col.startswith("jurisprudencia"):
        corpo = f"""{titulo_pt()}
  OPTIONAL {{ ?w cdm:work_date_document ?d }} OPTIONAL {{ ?w cdm:case-law_ecli ?ec }}"""
        campos = "(SAMPLE(?d) AS ?data) (SAMPLE(?ec) AS ?ecli) (SAMPLE(?t) AS ?titulo)"
        corpo_i = "?w cdm:case-law_interpretes_resource_legal ?x . ?x cdm:resource_legal_id_celex ?b ."
        campos_i = '(GROUP_CONCAT(DISTINCT ?b; separator=" ") AS ?interpreta)'
        so = citados_no_corpus() if col == "jurisprudencia-curada" else None
        if so is None:
            linhas = por_tipo("6", TIPOS_JURIS, corpo, campos)
            interp = por_tipo("6", TIPOS_JURIS, corpo_i, campos_i)
        else:  # poucos documentos: pedir só esses (em lotes), em vez de percorrer toda a jurisprudência
            linhas, interp = por_celex(sorted(so), corpo, campos), por_celex(sorted(so), corpo_i, campos_i)
        interp = {l["celex"]: l["interpreta"] for l in interp}
        for l in linhas:
            c = l["celex"]
            if so is not None and c not in so:
                continue
            actos[c] = {"celex": c, "tipo": TIPOS_JURIS.get(c[5:7], "Jurisprudência"), "data": l.get("data", "")[:10],
                        "ecli": l.get("ecli", ""), "titulo": eurlex.limpar_titulo(l.get("titulo", "")),
                        "interpreta": sorted(set(interp.get(c, "").split()) - {c})}
        if so is not None:
            faltam = sorted(so - set(actos))
            (CACHE / col).mkdir(parents=True, exist_ok=True)
            (CACHE / col / "sem-texto-pt.json").write_text(json.dumps(faltam), encoding="utf-8")
    elif col == "orientacoes":
        linhas = por_tipo("5", ["XC"], f"""{titulo_pt()}
  OPTIONAL {{ ?w cdm:work_date_document ?d }}""", "(SAMPLE(?d) AS ?data) (SAMPLE(?t) AS ?titulo)")
        for l in linhas:
            t = eurlex.limpar_titulo(l.get("titulo", ""))
            if "R(" in l["celex"] or not re.search(RE_ORIENTACOES, t, re.I) or re.search(EXCLUIR_ORIENTACOES, t, re.I):
                continue
            actos[l["celex"]] = {"celex": l["celex"], "tipo": "Comunicação da Comissão (JO C)",
                                 "data": l.get("data", "")[:10], "titulo": t}
    elif col == "revogada":
        em_ue = set()
        with open(RAIZ / "ue" / "INDICE.tsv", encoding="utf-8", newline="") as fh:
            em_ue = {l["celex"] for l in csv.DictReader(fh, delimiter="\t")}
        linhas = por_tipo("3", TIPOS_3, f"""?w cdm:resource_legal_in-force ?f . FILTER(STR(?f) IN ("false", "0"))
  FILTER NOT EXISTS {{ ?w cdm:resource_legal_in-force ?f2 . FILTER(STR(?f2) IN ("true", "1")) }}
  {titulo_pt()}
  OPTIONAL {{ ?w cdm:work_date_document ?d }} OPTIONAL {{ ?w cdm:resource_legal_date_end-of-validity ?fim }}""",
                         "(SAMPLE(?d) AS ?data) (SAMPLE(?t) AS ?titulo) (SAMPLE(?fim) AS ?fim_validade)", anos=ANOS)
        versoes = {}
        for base, cc, d in eurlex.versoes_consolidadas_todas():
            versoes.setdefault(base, []).append((cc, d))
        for l in linhas:
            c = l["celex"]
            if c in em_ue or "R(" in c:
                continue
            actos[c] = {"celex": c, "tipo": eurlex.nome_tipo(c), "data": l.get("data", "")[:10],
                        "titulo": eurlex.limpar_titulo(l.get("titulo", "")),
                        "fim_validade": (l.get("fim_validade") or "")[:10],
                        "versoes": sorted(set(map(tuple, versoes.get(c, []))), key=lambda v: v[1], reverse=True)}
    elif col == "propostas":
        linhas = por_tipo("5", ["PC"], f"""{titulo_pt()}
  OPTIONAL {{ ?w cdm:work_date_document ?d }}""", "(SAMPLE(?d) AS ?data) (SAMPLE(?t) AS ?titulo)")
        for l in linhas:
            if "R(" in l["celex"]:
                continue
            actos[l["celex"]] = {"celex": l["celex"], "tipo": "Proposta da Comissão (COM)",
                                 "data": l.get("data", "")[:10], "titulo": eurlex.limpar_titulo(l.get("titulo", ""))}
    (CACHE / col).mkdir(parents=True, exist_ok=True)
    (CACHE / col / "lista.json").write_text(json.dumps({"data": hoje, "actos": actos}, ensure_ascii=False),
                                            encoding="utf-8")
    print(f"{col}: {len(actos)} documentos na lista")
    return actos


def lista(col):
    return json.loads((CACHE / col / "lista.json").read_text(encoding="utf-8"))["actos"]


# ---------------------------------------------------------------------------
# Descarga
# ---------------------------------------------------------------------------

def _cache(col, celex):
    # A jurisprudência curada partilha a cache com a completa (os mesmos documentos).
    c = "jurisprudencia" if col.startswith("jurisprudencia") else col
    return CACHE / c / "html" / celex[1:5] / f"{completo.nome_ficheiro(celex)}.json.gz"


def descarregar_um(col, a, hoje):
    destino = _cache(col, a["celex"])
    if destino.exists():
        return "cache"
    reg = {"celex": a["celex"], "obtido_em": hoje}
    for cc, d in a.get("versoes", []):  # legislação revogada: última versão consolidada com texto PT
        if d > hoje:
            continue
        html, fmt = completo.conteudo(cc)
        if html:
            reg.update(texto=html, formato=fmt, versao=cc, versao_data=d)
            break
    if "texto" not in reg:
        html, fmt = completo.conteudo(a["celex"])
        if html:
            reg.update(texto=html, formato=fmt)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(destino, "wt", encoding="utf-8") as fh:
        json.dump(reg, fh, ensure_ascii=False)
    return "ok" if "texto" in reg else "sem texto"


def cmd_descarregar(col, fios=8):
    actos = lista(col)
    hoje = dt.date.today().isoformat()
    alvo = sorted(actos.values(), key=lambda a: a["celex"], reverse=True)
    feitos, estados, inicio = 0, {}, time.time()
    with cf.ThreadPoolExecutor(max_workers=fios) as ex:
        futs = {ex.submit(descarregar_um, col, a, hoje): a["celex"] for a in alvo}
        for f in cf.as_completed(futs):
            try:
                e = f.result()
            except Exception as err:  # noqa: BLE001 — registar e continuar
                e = f"erro: {err}"
                print(f"  {futs[f]}: {e}", file=sys.stderr)
            estados[e.split(":")[0]] = estados.get(e.split(":")[0], 0) + 1
            feitos += 1
            if feitos % 500 == 0 or feitos == len(alvo):
                print(f"{col}: {feitos}/{len(alvo)} {estados} {feitos / max(1, time.time() - inicio):.1f}/s", flush=True)
    return estados


# ---------------------------------------------------------------------------
# Conversão
# ---------------------------------------------------------------------------

# Títulos de partes dos acórdãos e despachos (linhas isoladas no texto do Cellar).
RE_PARTE_JURIS = re.compile(
    r"^(Quadro jurídico|Direito da União|Direito internacional|Direito (nacional|[a-záéíóúâêôãõç]+o)|"
    r"(O )?[Ll]itígio( no processo principal)?.{0,90}|Antecedentes do litígio.{0,60}|"
    r"Tramitação processual.{0,90}|Pedidos das partes.{0,60}|Quanto (à|ao|às|aos) .{3,120}|"
    r"Questões? prejudicia(l|is).{0,60}|Matéria de facto|Questão de direito|Os factos|"
    r"Pelos fundamentos expostos.{0,300}|Decisão sobre as despesas|Despesas)$")
RE_PARTE_CONCL = re.compile(r"^((I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\.)\s+\S.{0,140}$")
RE_SUB_CONCL = re.compile(r"^[A-H]\.\s+\S.{0,140}$")


def estruturar_juris(md):
    """Nos acórdãos, as disposições citadas (directivas, leis nacionais) aparecem como "### Artigo …";
    passam a texto em negrito, para não se confundirem com artigos do próprio documento, e as partes
    do acórdão (quadro jurídico, questões prejudiciais, decisão…) passam a títulos ##."""
    out = []
    for linha in md.splitlines():
        if linha.startswith("#"):
            linha = "**" + linha.lstrip("#").strip() + "**"
        elif re.match(r"^- (Pelos fundamentos expostos|Quanto às despesas)", linha) and len(linha) < 400:
            linha = "## " + linha[2:].strip()
        elif len(linha) < 200 and not linha.startswith(("-", "|", ">")):
            s = linha.strip()
            if RE_PARTE_JURIS.match(s) or RE_PARTE_CONCL.match(s):
                linha = "## " + s
            elif RE_SUB_CONCL.match(s):
                linha = "### " + s
        out.append(linha)
    return "\n".join(out)


def converter_um(col, raiz, a):
    c = _cache(col, a["celex"])
    if not c.exists():
        return None
    with gzip.open(c, "rt", encoding="utf-8") as fh:
        reg = json.load(fh)
    if "texto" not in reg:
        return {"celex": a["celex"], "data": a.get("data", ""), "tipo": a.get("tipo", ""),
                "titulo": a.get("titulo", "")[:200], "texto": "sem texto", "kb": 0, "ficheiro": ""}
    destino = ficheiro(col, raiz, a["celex"])
    destino.parent.mkdir(parents=True, exist_ok=True)
    partes = completo._corpo(reg["texto"], reg.get("formato"))
    corpo = partes["dispositivo"].strip()
    if col.startswith("jurisprudencia"):
        corpo = estruturar_juris(corpo)
    estado = ("consolidado" if reg.get("versao") else "original (JO)") + \
        {"pdf": " — PDF", "doc": " — Word"}.get(reg.get("formato"), "")
    fm = {"celex": a["celex"], "tipo": a.get("tipo"), "titulo": a.get("titulo"), "data_documento": a.get("data"),
          "ecli": a.get("ecli"), "interpreta": a.get("interpreta") or None,
          "estado": "não em vigor" if col == "revogada" else None,
          "fim_validade": a.get("fim_validade"), "texto": estado,
          "versao_consolidada": reg.get("versao"), "versao_aplicavel_desde": reg.get("versao_data"),
          "url_eurlex": eurlex.url_eurlex(a["celex"]), "obtido_em": reg.get("obtido_em")}
    fm = {k: v for k, v in fm.items() if v not in (None, "", [])}
    ls = [f"# {a.get('titulo') or a['celex']}", ""]
    if col == "revogada":
        fim = f" (fim de validade registado no Cellar: {a['fim_validade']})" if a.get("fim_validade") else ""
        ls += [f"**Já não está em vigor**{fim}. Serve para saber que regra se aplicava antes; para a regra "
               "actual, procurar o acto que o substituiu.", ""]
        if reg.get("versao"):
            ls += [f"**Texto:** última versão consolidada com texto em português, aplicável desde "
                   f"{reg['versao_data']} ({reg['versao']}). Versões anteriores: EUR-Lex.", ""]
        else:
            ls += ["**Texto:** versão original publicada no Jornal Oficial (sem as alterações posteriores).", ""]
    elif col == "orientacoes":
        ls += ["**Não é legislação:** comunicação da Comissão publicada no JO C. Explica como a Comissão "
               "interpreta e aplica as regras; não vincula os tribunais (quem interpreta é o Tribunal de "
               "Justiça). Pode ter sido substituída por uma versão mais recente: confirmar no EUR-Lex.", ""]
    elif col == "propostas":
        ls += ["**Não é legislação:** proposta da Comissão. Pode ter sido adoptada (com alterações), retirada "
               "ou estar ainda em negociação; o estado do processo está no EUR-Lex.", ""]
    elif col.startswith("jurisprudencia"):
        if a.get("interpreta"):
            ls += ["**Interpreta:** " + ", ".join(a["interpreta"][:30]) + ".", ""]
    if partes.get("preambulo"):
        ls += ["## Preâmbulo", "", partes["preambulo"].strip(), ""]
    ls += ["## Texto", "", corpo]
    completo.escrever_em_partes(destino, eurlex._frontmatter(fm) + "\n".join(ls).rstrip() + "\n")
    return {"celex": a["celex"], "data": a.get("data", ""), "tipo": a.get("tipo", ""),
            "titulo": a.get("titulo", "")[:200], "texto": estado, "kb": destino.stat().st_size // 1024,
            "ficheiro": str(destino.relative_to(raiz)), "interpreta": " ".join(a.get("interpreta") or [])}


def _converter_lote(args):
    col, raiz, a = args
    return converter_um(col, raiz, a)


def cmd_converter(col, raiz, fios=4):
    actos = lista(col)
    base = destino_base(col, raiz)
    with cf.ProcessPoolExecutor(max_workers=fios, max_tasks_per_child=200) as ex:
        linhas = [r for r in ex.map(_converter_lote, [(col, raiz, a) for a in actos.values()], chunksize=20) if r]
    validos = {completo.nome_ficheiro(c) for c in actos}
    removidos = 0
    for f in base.glob("**/*.md"):
        b = re.sub(r"\.parte-\d+$", "", f.name[:-3])
        if f.parent != base and b not in validos:
            f.unlink()
            removidos += 1
    campos = ["celex", "data", "tipo", "titulo", "texto", "kb", "ficheiro"] + \
        (["interpreta"] if col.startswith("jurisprudencia") else [])
    base.mkdir(parents=True, exist_ok=True)
    with open(base / "INDICE.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(campos)
        for l in sorted(linhas, key=lambda x: x["celex"]):
            w.writerow([str(l.get(k, "")).replace("\t", " ").replace("\n", " ") for k in campos])
    com = sum(1 for l in linhas if l["ficheiro"])
    print(f"{col}: {com} ficheiros escritos, {len(linhas) - com} sem texto, {removidos} removidos")
    return linhas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("passo", choices=["listas", "descarregar", "converter", "tudo"])
    ap.add_argument("colecao", choices=["jurisprudencia-curada", "orientacoes", "jurisprudencia", "revogada",
                                        "propostas"])
    ap.add_argument("--raiz", type=pathlib.Path, default=RAIZ, help="repositório de destino (por omissão, este)")
    ap.add_argument("--fios", type=int, default=8)
    a = ap.parse_args()
    raiz = a.raiz.resolve()
    if a.passo in ("listas", "tudo"):
        cmd_listas(a.colecao)
    if a.passo in ("descarregar", "tudo"):
        cmd_descarregar(a.colecao, a.fios)
    if a.passo in ("converter", "tudo"):
        cmd_converter(a.colecao, raiz)


if __name__ == "__main__":
    main()
