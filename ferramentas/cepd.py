#!/usr/bin/env python3
"""Orientações do Comité Europeu para a Proteção de Dados (CEPD / EDPB): diretrizes, recomendações
e outras orientações sobre o RGPD e legislação conexa, em orientacoes/cepd/.

  python3 ferramentas/cepd.py     percorre edpb.europa.eu/documents_en, obtém cada documento dos
                                  tipos escolhidos e escreve orientacoes/cepd/<ano>/<nome>.md e
                                  orientacoes/cepd/INDICE.tsv

Texto: o PDF em português quando o CEPD o publica (as versões adoptadas depois de consulta pública
costumam ser traduzidas; as recentes e as submetidas a consulta, muitas vezes só em inglês); senão,
o PDF em inglês, assinalado. 1 s entre pedidos; PDFs em .cache/cepd/.

Reutilização: "The reuse of any information of this website is authorized for commercial and
non-commercial purposes", com indicação da fonte e sem distorcer o sentido
(https://www.edpb.europa.eu/copyright_en, consultado em 2026-10-10).
"""

import csv
import hashlib
import datetime as dt
import html
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "orientacoes" / "cepd"
CACHE = RAIZ / ".cache" / "cepd"
BASE = "https://www.edpb.europa.eu"
UA = "Mozilla/5.0 (compatible; eur-lex-corpus/1.0; +https://github.com/HNFerramentasHitNails/eur-lex)"
# Tipos de documento do site que são orientações gerais (fora: pareceres sobre decisões de autoridades
# nacionais, decisões vinculativas em litígios concretos, cartas, actas…).
TIPOS = {"guideline": "Diretrizes", "recommendation": "Recomendações", "other-guidance": "Outras orientações",
         "statement": "Declaração"}
_ultimo = [0.0]


def obter(url, binario=False):
    espera = 1.0 - (time.time() - _ultimo[0])
    if espera > 0:
        time.sleep(espera)
    for n in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                dados = r.read()
            _ultimo[0] = time.time()
            return dados if binario else dados.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            _ultimo[0] = time.time()
            if e.code == 404:
                return None
            if n == 2:
                print(f"  falhou {url}: {e}", file=sys.stderr)
                return None
        except Exception as e:  # noqa: BLE001 — rede: tentar de novo e, à 3.ª, desistir deste URL
            _ultimo[0] = time.time()
            if n == 2:
                print(f"  falhou {url}: {e}", file=sys.stderr)
                return None
        time.sleep(4 * (n + 1))


def limpo(x):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x or ""))).strip()


def documentos():
    """[(tipo, url)] de todas as páginas da lista de documentos."""
    res, pagina, vazias = {}, 0, 0
    while vazias < 2 and pagina < 200:
        t = obter(f"{BASE}/documents_en?page={pagina}") or ""
        novos = 0
        for tipo, slug in re.findall(r'href="/documents/([a-z0-9-]+)/([^"#?]+?)_en"', t):
            if tipo in TIPOS and slug not in res:
                res[slug] = (tipo, f"{BASE}/documents/{tipo}/{slug}_en")
                novos += 1
        vazias = vazias + 1 if not re.search(r'href="/documents/[a-z0-9-]+/', t) else 0
        pagina += 1
    print(f"{len(res)} documentos dos tipos {', '.join(TIPOS)} em {pagina} páginas da lista")
    return list(res.values())


def pdf_texto(dados):
    with subprocess.Popen(["pdftotext", "-layout", "-enc", "UTF-8", "-", "-"], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as p:
        out, _ = p.communicate(dados, timeout=300)
    return out.decode("utf-8", errors="replace")


def escolher_pdf(pdfs):
    """PDF principal em português, senão em inglês (fora relatórios de consulta, anexos e versões
    com marcas de alterações)."""
    def principal(u):
        n = u.rsplit("/", 1)[-1].lower()
        return not re.search(r"report|annex|anexo|track|statement-on-the-consultation|comments", n)
    for lingua in ("pt", "en"):
        cand = [u for u in pdfs if re.search(rf"[_-]{lingua}(_\d+)?\.pdf$", u.lower()) and principal(u)]
        if cand:
            return cand[0], lingua
    return None, None  # só noutras línguas (ex.: documentos de autoridades nacionais anexos): fica só o índice


def tratar(tipo, url):
    nome = url.rsplit("/", 1)[-1].removesuffix("_en")
    pag = obter(url) or ""
    pag_pt = obter(url[:-3] + "_pt") or ""
    titulo_en = limpo((re.search(r"<h1[^>]*>(.*?)</h1>", pag, re.S) or [None, ""])[1])
    titulo_pt = limpo((re.search(r"<h1[^>]*>(.*?)</h1>", pag_pt, re.S) or [None, ""])[1])
    data = (re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})', pag) or [None, ""])[1]
    pdfs = []
    for h in re.findall(r'href="([^"]+\.pdf)"', pag + pag_pt):
        u = urllib.parse.urljoin(BASE, html.unescape(h))
        if u not in pdfs:
            pdfs.append(u)
    pdf, lingua = escolher_pdf(pdfs)
    reg = {"nome": nome, "tipo": TIPOS[tipo], "titulo": titulo_pt or titulo_en, "titulo_en": titulo_en,
           "data": data, "pagina": url, "pdf": pdf or "", "lingua": lingua or "", "ficheiro": ""}
    if not pdf:
        return reg
    CACHE.mkdir(parents=True, exist_ok=True)
    c = CACHE / (hashlib.sha1(pdf.encode()).hexdigest()[:16] + ".pdf")
    if not c.exists():
        dados = obter(pdf, binario=True)
        if not dados:
            return reg
        c.write_bytes(dados)
    texto = pdf_texto(c.read_bytes())
    texto = re.sub(r"[ \t]+\n", "\n", texto).replace("\f", "\n")
    ano = (data or "0000")[:4]
    destino = SAIDA / ano / f"{nome}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    fm = ["---", f"titulo: {json.dumps(reg['titulo'], ensure_ascii=False)}",
          f"titulo_en: {json.dumps(titulo_en, ensure_ascii=False)}", f"tipo: {reg['tipo']}",
          f"autor: Comité Europeu para a Proteção de Dados (CEPD / EDPB)", f"data: '{data}'",
          f"lingua: {'português' if lingua == 'pt' else 'inglês' if lingua == 'en' else 'desconhecida'}",
          f"pagina: {url}", f"pdf: {pdf}", f"obtido_em: '{dt.date.today().isoformat()}'",
          "fonte: © Comité Europeu para a Proteção de Dados — reutilização autorizada com indicação da fonte "
          "(edpb.europa.eu/copyright_en)", "---", ""]
    cab = [f"# {reg['titulo']}", "",
           "**Não é legislação:** orientação do CEPD sobre a aplicação do RGPD (ou de legislação conexa). Não "
           "vincula os tribunais, mas as autoridades de proteção de dados (em Portugal, a CNPD) seguem-na. "
           "Texto extraído automaticamente do PDF: quebras de linha e tabelas podem estar desalinhadas.", ""]
    if lingua != "pt":
        cab += ["**Língua:** o CEPD não publicou versão portuguesa deste documento (verificado nas páginas em "
                "inglês e português); o texto abaixo está em **inglês**.", ""]
    destino.write_text("\n".join(fm + cab) + "## Texto\n\n```text\n" + texto.strip() + "\n```\n", encoding="utf-8")
    reg["ficheiro"] = str(destino.relative_to(RAIZ))
    return reg


def main():
    docs = documentos()
    linhas = []
    for i, (tipo, url) in enumerate(docs, 1):
        linhas.append(tratar(tipo, url))
        if i % 20 == 0:
            print(f"  {i}/{len(docs)}", flush=True)
    validos = {l["ficheiro"] for l in linhas if l["ficheiro"]}
    for f in SAIDA.glob("*/*.md"):
        if str(f.relative_to(RAIZ)) not in validos:
            f.unlink()
    campos = ["data", "tipo", "titulo", "lingua", "ficheiro", "pagina", "pdf"]
    with open(SAIDA / "INDICE.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(campos)
        for l in sorted(linhas, key=lambda x: (x["data"], x["nome"]), reverse=True):
            w.writerow([str(l.get(k, "")).replace("\t", " ") for k in campos])
    pt = sum(1 for l in linhas if l["lingua"] == "pt" and l["ficheiro"])
    en = sum(1 for l in linhas if l["lingua"] != "pt" and l["ficheiro"])
    print(f"{len(linhas)} documentos; {pt} com texto em português, {en} só noutra língua, "
          f"{len(linhas) - pt - en} sem PDF")


if __name__ == "__main__":
    main()
