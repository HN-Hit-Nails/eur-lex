#!/usr/bin/env python3
"""Códigos tributários portugueses tal como a Autoridade Tributária e Aduaneira (AT) os publica no
Portal das Finanças (texto actualizado, artigo a artigo, com a indicação "Redação da Lei …").

  python3 ferramentas/at_codigos.py     escreve legislacao-pt/codigo-iva.md (Código do IVA)

Porquê a AT e não o DRE: o identificador europeu ELI do Código do IVA (Decreto-Lei n.º 394-B/84)
no DRE leva a uma página de consolidação que o próprio DRE marca como não publicada (página de
erro), e o ELI do diploma original não resolve (verificado em 2026-10-10).

A compilação da AT não é a publicação oficial: faz fé o Diário da República. 1 s entre pedidos;
páginas em .cache/at/.
"""

import datetime as dt
import html
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CACHE = RAIZ / ".cache" / "at"
UA = "Mozilla/5.0 (compatible; eur-lex-corpus/1.0; +https://github.com/HNFerramentasHitNails/eur-lex)"
BASE = "https://info.portaldasfinancas.gov.pt"
CODIGOS = {
    "codigo-iva": {
        "nome": "Código do Imposto sobre o Valor Acrescentado (CIVA)",
        "diploma": "Decreto-Lei n.º 394-B/84, de 26 de dezembro (aprova o Código do IVA)",
        "indice": BASE + "/pt/informacao_fiscal/codigos_tributarios/civa_rep/Pages/codigo-do-iva-indice.aspx",
        "paginas": r"(?:ivapreambulo|iva\d+[a-z]?|artigo-\d+-o-do-civa|c-iva-listas)\.aspx",
        "relacionado_com": ["32006L0112"],
    },
}
_ultimo = [0.0]


def obter(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    c = CACHE / re.sub(r"[^A-Za-z0-9._-]", "_", urllib.parse.urlsplit(url).path.rsplit("/", 1)[-1])
    if c.exists() and c.stat().st_mtime > time.time() - 6 * 3600:
        return c.read_text(encoding="utf-8")
    espera = 1.0 - (time.time() - _ultimo[0])
    if espera > 0:
        time.sleep(espera)
    for n in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                t = r.read().decode("utf-8", errors="replace")
            _ultimo[0] = time.time()
            c.write_text(t, encoding="utf-8")
            return t
        except Exception as e:  # noqa: BLE001 — rede: tentar de novo e, à 3.ª, desistir
            _ultimo[0] = time.time()
            if n == 2:
                print(f"  falhou {url}: {e}", file=sys.stderr)
                return None
            time.sleep(4 * (n + 1))


def conteudo(pag):
    """Texto do campo principal da página (SharePoint: RichHtmlField), em linhas."""
    i = pag.find("RichHtmlField")
    if i < 0:
        return []
    fim = [j for j in (pag.find("SummaryLinkFieldControl", i), pag.find("ctl03_label", i)) if j > 0]
    t = pag[pag.find(">", i) + 1:min(fim) if fim else len(pag)]
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</(p|div|h\d|li|tr)>", "\n", t)
    t = re.sub(r"(?i)</t[dh]>", " | ", t)
    t = re.sub("[\u200b\ufeff\r]", "", html.unescape(re.sub(r"<[^>]+>", "", t)))
    linhas = (re.sub(r"\s+", " ", l).strip(" |") for l in t.split("\n"))
    return [l for l in linhas if l]


def md_pagina(linhas):
    """Artigo N.º + epígrafe -> "### Artigo N.º — epígrafe"; capítulos e secções -> "##"."""
    out, i = [], 0
    while i < len(linhas):
        l = linhas[i]
        m = re.match(r"^Artigo (\d+)\.\s?º\s*(?:-\s*([A-Z]))?\s*(\(\*\))?$", l)
        if m:
            l = f"Artigo {m.group(1)}.º" + (f"-{m.group(2)}" if m.group(2) else "")
            nxt = linhas[i + 1] if i + 1 < len(linhas) else ""
            epi = nxt if nxt and len(nxt) < 150 and not re.match(r"^\d+ - |^[a-z]\) ", nxt) \
                and not nxt.endswith((".", ";", ":")) else ""
            out.append(f"### {l} — {epi}" if epi else f"### {l}")
            i += 2 if epi else 1
            continue
        if re.match(r"^(CAPÍTULO|SECÇÃO|SUBSECÇÃO|TÍTULO|LISTA|ANEXO)\b", l) and len(l) < 90:
            nxt = linhas[i + 1] if i + 1 < len(linhas) else ""
            if nxt and len(nxt) < 120 and not re.match(r"^(Artigo|\d+ - )", nxt):
                out.append(f"## {l} — {nxt}")
                i += 2
                continue
            out.append(f"## {l}")
        elif l.startswith("(Redação") or l.startswith("(Aditado") or l.startswith("(Revogado"):
            out.append(f"> {l}")
        elif re.match(r"^CÓDIGO DO IMPOSTO", l):
            pass
        else:
            out.append(l)
        i += 1
    return "\n\n".join(out)


def gerar(chave):
    cfg = CODIGOS[chave]
    indice = obter(cfg["indice"]) or ""
    urls = []
    for h in re.findall(r'href="([^"#]*?' + cfg["paginas"] + r')"', indice, re.I):
        u = urllib.parse.urljoin(cfg["indice"], html.unescape(h))
        if u not in urls:
            urls.append(u)
    partes, vistos = [], set()
    for u in urls:
        p = obter(u)
        if not p:
            partes.append(f"> Página não obtida: {u}")
            continue
        md = md_pagina(conteudo(p))
        if md and md not in vistos:
            vistos.add(md)
            partes.append(md)
    hoje = dt.date.today().isoformat()
    n_art = sum(p.count("### Artigo") for p in partes)
    fm = ["---", f"diploma: {cfg['nome']}", f"aprovado_por: {cfg['diploma']}",
          "texto: actualizado (compilação da AT, Portal das Finanças)", f"relacionado_com: {cfg['relacionado_com']}",
          f"url: {cfg['indice']}", "fonte: Autoridade Tributária e Aduaneira — Portal das Finanças",
          f"obtido_em: '{hoje}'", "---", ""]
    cab = [f"# {cfg['nome']}", "", f"**Aprovado por:** {cfg['diploma']}.", "",
           "**Texto:** compilação actualizada publicada pela Autoridade Tributária e Aduaneira no Portal das "
           "Finanças, artigo a artigo; as linhas `> (Redação …)` indicam o diploma que deu a redacção actual. "
           "Não é a publicação oficial: faz fé o Diário da República. Obtida da AT porque o DRE não tem a "
           "consolidação deste código disponível pelo identificador ELI (página de erro, verificado em "
           f"2026-10-10). {n_art} artigos obtidos de {len(urls)} páginas.", "",
           f"**Fonte:** {cfg['indice']}", "", "## Texto", ""]
    destino = RAIZ / "legislacao-pt" / f"{chave}.md"
    destino.write_text("\n".join(fm + cab) + "\n\n".join(partes) + "\n", encoding="utf-8")
    print(f"{destino.relative_to(RAIZ)}: {n_art} artigos, {len(urls)} páginas")


if __name__ == "__main__":
    for k in CODIGOS:
        gerar(k)
