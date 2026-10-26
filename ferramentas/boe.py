#!/usr/bin/env python3
"""Legislação espanhola tal como o Boletín Oficial del Estado (BOE) a publica consolidada, pela API de
dados abertos (https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/<identificador>/texto).

  python3 ferramentas/boe.py     escreve legislacao-es/<chave>.md e legislacao-es/INDICE.md

Para uma empresa em Espanha, a regra aplicável é a lei espanhola (a Diretiva IVA só fixa os limites,
por exemplo o art. 252.º: o prazo da declaração fixa-o cada Estado-Membro). Por agora, o IVA e as
leis gerais de que dependem os seus prazos (a Ley General Tributaria e a do procedimento administrativo).

Texto em espanhol, sem tradução. Cada bloco do BOE traz as suas versões; usa-se a última já aplicável
(`fecha_vigencia` até hoje) e as posteriores ficam anotadas. O texto consolidado do BOE não tem valor
jurídico: faz fé o publicado no BOE. 1 s entre pedidos; respostas em .cache/boe/.
"""

import datetime as dt
import pathlib
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CACHE = RAIZ / ".cache" / "boe"
DESTINO = RAIZ / "legislacao-es"
UA = "Mozilla/5.0 (compatible; eur-lex-corpus/1.0; +https://github.com/HNFerramentasHitNails/eur-lex)"
API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/"
NORMAS = {
    "ley-37-1992": {"id": "BOE-A-1992-28740", "relacionado_com": ["32006L0112"],
                    "nota": "Lei do IVA espanhola."},
    "real-decreto-1624-1992": {"id": "BOE-A-1992-28925", "relacionado_com": ["32006L0112"],
                               "nota": "Aprova o Reglamento del IVA (em anexo; os artigos do regulamento "
                                       "vêm depois de `## Anexo`)."},
    "orden-eha-3786-2008": {"id": "BOE-A-2008-20953", "relacionado_com": ["32006L0112"],
                            "nota": "Aprova o modelo 303 (autoliquidação do IVA) e os seus prazos."},
    "ley-58-2003": {"id": "BOE-A-2003-23186", "relacionado_com": [],
                    "nota": "Ley General Tributaria (art. 7.º, n.º 2, e art. 97.º: o direito administrativo geral é supletivo)."},
    "ley-39-2015": {"id": "BOE-A-2015-10565", "relacionado_com": [],
                    "nota": "Procedimento administrativo comum (art. 30.º: cômputo dos prazos e o último dia inhábil)."},
    "orden-eha-1658-2009": {"id": "BOE-A-2009-10326", "relacionado_com": [],
                            "nota": "Domiciliação bancária do pagamento das autoliquidações (art. 3.º e anexo II: os prazos de "
                                    "quem paga por débito directo, por modelo, o 303 incluído)."},
    "resolucion-aeat-2009-12-28": {"id": "BOE-A-2009-21051", "relacionado_com": [],
                                   "nota": "Cria a sede electrónica e o registo electrónico da AEAT (Quinto, n.º 2: aplica-se o "
                                           "calendário de dias inhábiles da AEAT; Tercero, a): publicado na própria sede)."},
}
_ultimo = [0.0]


def obter(url, nome):
    CACHE.mkdir(parents=True, exist_ok=True)
    c = CACHE / nome
    if c.exists() and c.stat().st_mtime > time.time() - 6 * 3600:
        return c.read_bytes()
    espera = 1.0 - (time.time() - _ultimo[0])
    if espera > 0:
        time.sleep(espera)
    for n in range(3):
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/xml"})
            with urllib.request.urlopen(pedido, timeout=120) as r:
                b = r.read()
            _ultimo[0] = time.time()
            c.write_bytes(b)
            return b
        except Exception as e:  # noqa: BLE001 — rede: tentar de novo e, à 3.ª, desistir
            _ultimo[0] = time.time()
            if n == 2:
                print(f"  falhou {url}: {e}", file=sys.stderr)
                return None
            time.sleep(4 * (n + 1))


def texto(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def data(aaaammdd):
    return f"{aaaammdd[:4]}-{aaaammdd[4:6]}-{aaaammdd[6:8]}" if aaaammdd and len(aaaammdd) >= 8 else ""


def versao_aplicavel(bloco, hoje):
    """Última versão do bloco com fecha_vigencia até hoje, e as datas das posteriores (futuras)."""
    vs = bloco.findall("version")
    ja = [v for v in vs if (v.get("fecha_vigencia") or "0") <= hoje]
    futuras = [data(v.get("fecha_vigencia")) for v in vs if (v.get("fecha_vigencia") or "0") > hoje]
    return (ja[-1] if ja else None), futuras


def nota_visivel(bq, hoje):
    """As notas «Téngase en cuenta…» do BOE só valem até uma data (caduca, ou a classe noDesdeAAAAMMDD)."""
    if (bq.get("caduca") or "99999999") <= hoje:
        return False
    m = re.match(r"noDesde(\d{8})", bq.get("class") or "")
    return not (m and m.group(1) <= hoje)


def md_bloco(bloco, versao, hoje):
    tipo, titulo = bloco.get("tipo"), re.sub(r"\s+", " ", bloco.get("titulo") or "").strip()  # o BOE às vezes usa \xa0
    out, cab = [], []
    for p in versao:
        cls = p.get("class") or ""
        if p.tag == "blockquote":
            if nota_visivel(p, hoje):
                out += [f"> {texto(x)}" for x in p if texto(x)]
            continue
        if p.tag == "table":
            for tr in p.iter("tr"):
                cel = [texto(td) for td in tr if td.tag in ("td", "th")]
                if any(cel):
                    out.append("| " + " | ".join(cel) + " |")
            continue
        t = texto(p)
        if not t:
            continue
        if cls == "imagen":
            out.append("> [imagem no original do BOE]")
        elif cls in ("titulo_num", "capitulo_num", "seccion", "anexo_num", "anexo", "subseccion") and tipo == "encabezado":
            cab.append(t)
        elif cls in ("titulo_tit", "capitulo_tit", "anexo_tit") and tipo == "encabezado":
            cab.append(t)
        elif cls == "articulo" and tipo == "precepto":
            epi = t[len(titulo):].lstrip(". ").strip() if t.startswith(titulo) else t
            out.insert(0, f"### {titulo or t} — {epi}" if epi and titulo else f"### {t}")
        else:
            out.append(t)
    if tipo == "encabezado":
        nome = cab[0] if cab else titulo
        nome = re.sub(r"(?i)^anexo\b", "Anexo", nome)
        resto = " ".join(cab[1:])
        return [f"## {nome} — {resto}" if resto else f"## {nome}"] + out
    if tipo == "preambulo":
        return ["## Preâmbulo"] + out
    if tipo == "firma":
        return out
    if tipo == "nota_inicial":
        return [f"> {x}" for x in out]
    return out


def gerar(chave, hoje):
    cfg = NORMAS[chave]
    meta = obter(API + cfg["id"] + "/metadatos", cfg["id"] + ".meta.xml")
    corpo = obter(API + cfg["id"] + "/texto", cfg["id"] + ".texto.xml")
    if not meta or not corpo:
        print(f"{chave}: não obtido (o ficheiro anterior fica)", file=sys.stderr)
        return None
    m = ET.fromstring(meta).find(".//metadatos")
    titulo = m.findtext("titulo")
    actualizado = data(m.findtext("fecha_actualizacion") or "")
    partes, futuras, n_art, anterior = [], set(), 0, None
    for b in ET.fromstring(corpo).iter("bloque"):
        v, fut = versao_aplicavel(b, hoje)
        futuras.update(fut)
        if v is None:
            continue
        linhas = md_bloco(b, v, hoje)
        if anterior == "preambulo" and b.get("tipo") == "precepto":
            linhas = ["## Articulado"] + linhas  # fecha o preâmbulo antes dos artigos (sem título nem capítulo)
        anterior = b.get("tipo") if linhas else anterior
        n_art += sum(1 for l in linhas if l.startswith("### "))
        if linhas:
            partes.append("\n\n".join(linhas))
    url = f"https://www.boe.es/buscar/act.php?id={cfg['id']}"
    fm = ["---", f"diploma: {titulo}", f"identificador: {cfg['id']}",
          "texto: consolidado (BOE, legislación consolidada)", f"relacionado_com: {cfg['relacionado_com']}",
          f"url: {url}", "fonte: Agencia Estatal Boletín Oficial del Estado — API de dados abertos",
          "lingua: es", f"consolidado_ate: '{actualizado}'",
          f"versoes_futuras: {sorted(futuras)}", f"obtido_em: '{dt.date.today().isoformat()}'", "---", ""]
    cab = [f"# {titulo}", "", f"**Nota:** {cfg['nota']}", "",
           "**Texto:** versão consolidada do BOE (em espanhol), bloco a bloco, na última redacção já aplicável; "
           "as linhas `> Se modifica …` indicam o diploma que deu a redacção. Não tem valor jurídico: faz fé o "
           f"publicado no BOE. Consolidado pelo BOE até {actualizado}. {n_art} artigos e disposições."
           + (f" Há redacções que só se aplicam em: {', '.join(sorted(futuras))} (não incluídas)." if futuras else ""),
           "", f"**Fonte:** {url}", "", "## Texto", ""]
    DESTINO.mkdir(exist_ok=True)
    (DESTINO / f"{chave}.md").write_text("\n".join(fm + cab) + "\n\n".join(partes) + "\n", encoding="utf-8")
    print(f"legislacao-es/{chave}.md: {n_art} artigos e disposições, consolidado até {actualizado}")
    return {"chave": chave, "titulo": titulo, "actualizado": actualizado, "nota": cfg["nota"]}


def main():
    hoje = dt.date.today().strftime("%Y%m%d")
    feitas = [r for k in NORMAS if (r := gerar(k, hoje))]
    if len(feitas) < len(NORMAS) and (DESTINO / "INDICE.md").exists():
        return  # falhou alguma: o índice anterior continua certo
    linhas = ["# Legislação espanhola (BOE, consolidada)", "",
              "Normas espanholas obtidas do Boletín Oficial del Estado (texto consolidado, em espanhol). "
              "Gerado por `python3 ferramentas/boe.py`. Só o que já foi preciso: o IVA (lei, regulamento e "
              "o modelo 303) e, para contar os prazos, a Ley General Tributaria, a Ley 39/2015 e a Orden EHA/1658/2009 (débito directo) e a Resolución da AEAT de 28/12/2009 (a sede electrónica e o seu calendário). Para outra norma, acrescenta-se a `NORMAS` em `ferramentas/boe.py`.", "",
              "Consulta: `python3 ferramentas/procurar.py artigos real-decreto-1624-1992 plazo` e "
              "`python3 ferramentas/procurar.py ler real-decreto-1624-1992 71`.", ""]
    linhas += [f"- [{r['titulo'][:160]}]({r['chave']}.md) — consolidado até {r['actualizado']} — {r['nota']}"
               for r in feitas]
    (DESTINO / "INDICE.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
