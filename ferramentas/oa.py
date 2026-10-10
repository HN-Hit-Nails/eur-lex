#!/usr/bin/env python3
"""Ordem dos Advogados (portal.oa.pt): índice dos pareceres e texto dos regulamentos.

  pareceres     ordem-advogados/pareceres.tsv: órgão, período, título, assunto e ligações de cada
                parecer. Só o índice: o portal diz "Todos os direitos reservados" e não está
                decidido se os pareceres podem ser reproduzidos; o texto fica no portal.
  regulamentos  ordem-advogados/regulamentos/: texto (extraído do PDF) de cada acto da lista
                "Regulamentação aprovada pela OA" (deliberações e regulamentos publicados no
                Diário da República ou aprovados pelos órgãos da Ordem), com índice.
  tudo          os dois e ordem-advogados/INDICE.md

Respeita 1 s entre pedidos (o portal não tem robots.txt). Os PDFs ficam em .cache/oa/.
"""

import argparse
import csv
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

from bs4 import BeautifulSoup

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "ordem-advogados"
CACHE = RAIZ / ".cache" / "oa"
BASE = "https://portal.oa.pt"
UA = "Mozilla/5.0 (compatible; eur-lex-corpus/1.0; +https://github.com/HNFerramentasHitNails/eur-lex)"
PARECERES = "/advogados/pareceres-da-ordem/"
REGULAMENTOS = "/ordem/regras-profissionais/regulamentacao-aprovada-pela-oa/"
_ultimo = [0.0]


def seguro(url):
    """URL com o caminho e a consulta codificados (o portal usa º, ª e acentos nos endereços)."""
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(p.path, safe="/%:@!$&'()*+,;=-._~"),
                                    urllib.parse.quote(p.query, safe="=&%/:+,;-._~"), ""))


def obter(url, binario=False):
    espera = 1.0 - (time.time() - _ultimo[0])
    if espera > 0:
        time.sleep(espera)
    for n in range(3):
        try:
            req = urllib.request.Request(seguro(url), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                dados = r.read()
            _ultimo[0] = time.time()
            return dados if binario else dados.decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001 — rede: tentar de novo e, à 3.ª, desistir deste URL
            _ultimo[0] = time.time()
            if n == 2:
                print(f"  falhou {url}: {e}", file=sys.stderr)
                return None
            time.sleep(4 * (n + 1))


def absoluto(href):
    return urllib.parse.urljoin(BASE + "/", html.unescape(href))


def caminho(url):
    return urllib.parse.unquote(urllib.parse.urlsplit(url).path)


def limpo(x):
    return re.sub(r"\s+", " ", x or "").strip()


def itens(soup):
    """Itens das listas do portal: <a class="content-news-list__action"> com título (h3) e assunto."""
    res = []
    for a in soup.select("a.content-news-list__action"):
        h3 = a.find("h3")
        p = a.find("p")
        res.append({"url": absoluto(a["href"]), "titulo": limpo(h3.get_text(" ") if h3 else a.get_text(" ")),
                    "assunto": limpo(re.sub(r"^\s*Assunto\s*:\s*", "", p.get_text(" "))) if p else ""})
    return res


def ligacoes(soup, prefixo):
    """Outras páginas da mesma secção (subsecções, anos, paginação)."""
    res = set()
    for a in soup.find_all("a", href=True):
        if "content-news-list__action" in (a.get("class") or []):
            continue
        u = absoluto(a["href"])
        if urllib.parse.urlsplit(u).netloc != "portal.oa.pt":
            continue
        p = urllib.parse.urlsplit(u)
        if caminho(u).startswith(prefixo):
            res.add(urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, p.query, "")))
    return res


def pdfs(soup):
    return [absoluto(a["href"]) for a in soup.find_all("a", href=True) if a["href"].lower().split("?")[0].endswith(".pdf")]


def percorrer(prefixo, max_paginas=4000):
    """Percorre uma secção do portal. O portal usa o mesmo cartão para subsecções e para actos:
    uma página com cartões é uma lista (percorre-se), uma página sem cartões é um acto (parecer ou
    regulamento) e dá-se-lhe o título e o assunto do cartão que levou a ela."""
    vistos, fila, cartoes, actos = set(), [BASE + prefixo], {}, {}
    while fila and len(vistos) < max_paginas:
        url = fila.pop(0)
        if url in vistos:
            continue
        vistos.add(url)
        if url.lower().split("?")[0].endswith(".pdf"):
            if url in cartoes:
                actos[url] = {**cartoes[url], "pdf": [url]}
            continue
        t = obter(url)
        if t is None:
            continue
        soup = BeautifulSoup(t, "lxml")
        its = itens(soup)
        if its:
            for it in its:
                cartoes.setdefault(it["url"], {**it, "lista": caminho(url)})
                if it["url"] not in vistos:
                    fila.append(it["url"])
            for u in sorted(ligacoes(soup, prefixo)):
                if u not in vistos:
                    fila.append(u)
        elif url in cartoes:
            actos[url] = {**cartoes[url], "pdf": pdfs(soup)}
    return list(actos.values()), len(vistos)


def nomes_orgaos():
    t = obter(BASE + PARECERES)
    soup = BeautifulSoup(t or "", "lxml")
    nomes = {}
    for a in soup.find_all("a", href=True):
        c = caminho(absoluto(a["href"]))
        if c.startswith(PARECERES) and c.count("/") == 4:
            nomes.setdefault(c.split("/")[3], re.split(r"\s+Consulte\b", limpo(a.get_text(" ")))[0])
    return nomes


def cmd_pareceres():
    nomes = nomes_orgaos()
    lista, n_paginas = percorrer(PARECERES)
    linhas = []
    for it in sorted(lista, key=lambda x: x["url"]):
        partes = caminho(it["url"]).strip("/").split("/")
        orgao = partes[2] if len(partes) > 2 else ""
        periodo = partes[3] if len(partes) > 4 else ""
        linhas.append([nomes.get(orgao, orgao), periodo, it["titulo"], it["assunto"], it["url"], " ".join(it["pdf"])])
    SAIDA.mkdir(exist_ok=True)
    with open(SAIDA / "pareceres.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["orgao", "periodo", "titulo", "assunto", "pagina", "pdf"])
        w.writerows(linhas)
    print(f"{len(linhas)} pareceres ({n_paginas} páginas visitadas)")
    return linhas


def pdf_texto(dados):
    with subprocess.Popen(["pdftotext", "-layout", "-enc", "UTF-8", "-", "-"], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as p:
        out, _ = p.communicate(dados, timeout=120)
    return out.decode("utf-8", errors="replace")


def nome_ficheiro(titulo, usados):
    base = re.sub(r"[^a-z0-9]+", "-", titulo.lower().translate(str.maketrans(
        "áàâãäéèêëíìîïóòôõöúùûüçº", "aaaaaeeeeiiiiooooouuuuco"))).strip("-")[:90].rstrip("-")
    nome, i = base, 2
    while nome in usados:
        nome, i = f"{base}-{i}", i + 1
    usados.add(nome)
    return nome


def cmd_regulamentos():
    lista, n_paginas = percorrer(REGULAMENTOS)
    destino = SAIDA / "regulamentos"
    destino.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    hoje = dt.date.today().isoformat()
    usados, linhas = set(), []
    for it in lista:
        url = it["url"]
        ligados = it["pdf"]
        nome = nome_ficheiro(it["titulo"], usados)
        texto, estado = "", "sem PDF na página"
        for i, pdf in enumerate(ligados):
            cache = CACHE / f"{nome}-{i}.pdf"
            if not cache.exists():
                dados = obter(pdf, binario=True)
                if dados:
                    cache.write_bytes(dados)
            if cache.exists():
                parte = pdf_texto(cache.read_bytes()).strip()
                texto += ("\n\n" if texto else "") + parte
        if ligados:
            estado = "texto extraído do PDF" if texto.strip() else "PDF sem texto extraível (imagem?)"
        fm = ["---", f"titulo: {json.dumps(it['titulo'], ensure_ascii=False)}", f"pagina_oa: {json.dumps(url)}",
              f"pdf: {json.dumps(ligados)}", f"estado: {estado}", f"obtido_em: '{hoje}'",
              "nota: Texto tal como publicado (não consolidado); pode ter sido alterado ou revogado depois. "
              "Para efeitos legais, confirmar no Diário da República.", "---", ""]
        corpo = [f"# {it['titulo']}", "", f"Fonte: [{url}]({url})", ""]
        if texto.strip():
            corpo += ["## Texto (extraído do PDF; quebras de linha e tabelas podem estar desalinhadas)", "",
                      "```text", texto.rstrip(), "```", ""]
        (destino / f"{nome}.md").write_text("\n".join(fm + corpo), encoding="utf-8")
        linhas.append([it["titulo"], estado, f"regulamentos/{nome}.md", url])
    with open(SAIDA / "regulamentos.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["titulo", "estado", "ficheiro", "pagina"])
        w.writerows(linhas)
    print(f"{len(linhas)} actos da lista de regulamentação ({n_paginas} páginas percorridas); "
          f"{sum(1 for l in linhas if l[1] == 'texto extraído do PDF')} com texto")
    return linhas


def cmd_indice():
    par = list(csv.DictReader(open(SAIDA / "pareceres.tsv", encoding="utf-8"), delimiter="\t")) \
        if (SAIDA / "pareceres.tsv").exists() else []
    reg = list(csv.DictReader(open(SAIDA / "regulamentos.tsv", encoding="utf-8"), delimiter="\t")) \
        if (SAIDA / "regulamentos.tsv").exists() else []
    por_orgao = {}
    for p in par:
        por_orgao[p["orgao"]] = por_orgao.get(p["orgao"], 0) + 1
    ls = ["# Ordem dos Advogados", "",
          f"Gerado por `python3 ferramentas/oa.py tudo` em {dt.date.today().isoformat()} a partir de "
          "[portal.oa.pt](https://portal.oa.pt). Não é legislação da UE: é regulação profissional dos advogados em "
          "Portugal.", "",
          "## Estatuto", "",
          "O Estatuto da Ordem dos Advogados (Lei n.º 145/2015) está em "
          "[`legislacao-pt/lei-145-2015.md`](../legislacao-pt/lei-145-2015.md) (versão consolidada do DRE). A "
          "deontologia profissional é o título III do Estatuto (artigos 88.º e seguintes).", "",
          f"## Regulamentos e deliberações ({len(reg)})", "",
          "Lista \"Regulamentação aprovada pela OA\" do portal, com o texto extraído dos PDFs em `regulamentos/`. "
          "Texto tal como publicado, sem consolidação: pode ter sido alterado ou revogado. Índice: "
          "[`regulamentos.tsv`](regulamentos.tsv).", ""]
    ls += [f"- [{r['titulo']}]({r['ficheiro']}) — {r['estado']}" for r in reg]
    ls += ["", f"## Pareceres ({len(par)})", "",
           "Só o índice ([`pareceres.tsv`](pareceres.tsv): órgão, período, título, assunto, página e PDF). O texto "
           "não foi copiado: o portal indica \"Todos os direitos reservados\" e não há autorização para o "
           "reproduzir. Para ler um parecer, abrir a ligação. Pesquisa: `rg -i 'incompatib' ordem-advogados/pareceres.tsv`.", ""]
    ls += [f"- {o or '(sem órgão)'}: {n}" for o, n in sorted(por_orgao.items(), key=lambda x: -x[1])]
    ls += ["", "## Outras referências (só ligações)", "",
           "- Código de Deontologia dos Advogados Europeus (CCBE) e Princípios Básicos das Nações Unidas relativos à "
           "função dos Advogados: https://portal.oa.pt/ordem/regras-profissionais/legislacao-internacional/",
           "- Diretiva 98/5/CE (exercício permanente da advocacia noutro Estado-Membro): "
           "[`ue/diretivas/1998/31998L0005.md`](../ue/diretivas/1998/31998L0005.md); Diretiva 77/249/CEE (prestação "
           "de serviços): [`ue/diretivas/1977/31977L0249.md`](../ue/diretivas/1977/31977L0249.md)",
           "- Guias do CCBE: https://portal.oa.pt/advogados/informacao-pratica-relevante/ccbe-guias-de-orientacao-noticias-e-newsletters/",
           "- Prevenção do branqueamento de capitais (dossier para advogados): "
           "https://portal.oa.pt/advogados/informacao-pratica-relevante/bcft-dossier/",
           "- Formação externa (cursos HELP do Conselho da Europa, ERA): https://portal.oa.pt/advogados/formacao-externa/",
           ""]
    (SAIDA / "INDICE.md").write_text("\n".join(ls), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("passo", choices=["pareceres", "regulamentos", "indice", "tudo"])
    a = ap.parse_args()
    if a.passo in ("pareceres", "tudo"):
        cmd_pareceres()
    if a.passo in ("regulamentos", "tudo"):
        cmd_regulamentos()
    cmd_indice()


if __name__ == "__main__":
    main()
