#!/usr/bin/env python3
"""Profissões jurídicas e respectivas competências, da classificação europeia ESCO, em português.

ESCO (European Skills, Competences, Qualifications and Occupations) é a classificação da Comissão
Europeia usada no Europass e no EURES (Decisão de Execução (UE) 2018/1020, em ue/decisoes/2018/).
Conteúdo da UE reutilizável nos termos da licença CC BY 4.0 (aviso legal da Comissão, para onde o
site da ESCO remete): © União Europeia, https://esco.ec.europa.eu.

  python3 ferramentas/esco.py    escreve competencias/esco-*.tsv e competencias/esco-transversais.md

Grupos ISCO incluídos: 2611 (advogados), 2612 (juízes e magistrados), 2619 (outros especialistas em
assuntos jurídicos), 3411 (técnicos de nível intermédio dos serviços jurídicos), com as
subprofissões de cada um. 0,5 s entre pedidos à API.
"""

import collections
import csv
import datetime as dt
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "competencias"
API = "https://ec.europa.eu/esco/api/resource/"
GRUPOS = ["C2611", "C2612", "C2619", "C3411"]
_ultimo = [0.0]


def pedir(tipo, uri):
    espera = 0.5 - (time.time() - _ultimo[0])
    if espera > 0:
        time.sleep(espera)
    url = API + tipo + "?" + urllib.parse.urlencode({"uri": uri, "language": "pt"})
    for n in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/json"}),
                                        timeout=60) as r:
                _ultimo[0] = time.time()
                return json.load(r)
        except Exception as e:  # noqa: BLE001 — rede: tentar de novo e, à 3.ª, desistir
            _ultimo[0] = time.time()
            if n == 2:
                print(f"  falhou {uri}: {e}", file=sys.stderr)
                return None
            time.sleep(3 * (n + 1))


def titulos(d, chave):
    return [x.get("title", "") for x in (d or {}).get("_links", {}).get(chave, []) or []]


def texto_pt(d, campo):
    v = (d or {}).get(campo) or {}
    if isinstance(v, dict):
        v = v.get("pt") or v.get("pt-PT") or {}
        if isinstance(v, dict):
            return v.get("literal", "")
        if isinstance(v, list):
            return "; ".join(v)
    return v if isinstance(v, str) else ""


def main():
    profissoes, fila = {}, []
    for g in GRUPOS:
        d = pedir("concept", f"http://data.europa.eu/esco/isco/{g}")
        for o in (d or {}).get("_links", {}).get("narrowerOccupation", []):
            fila.append((o["uri"], g, d.get("title", g)))
    while fila:
        uri, g, nome_g = fila.pop(0)
        if uri in profissoes:
            continue
        d = pedir("occupation", uri)
        if not d:
            continue
        profissoes[uri] = {"d": d, "grupo": g[1:], "nome_grupo": nome_g}
        for o in d.get("_links", {}).get("narrowerOccupation", []):
            fila.append((o["uri"], g, nome_g))
    competencias = {}
    for p in profissoes.values():
        for rel in ("hasEssentialSkill", "hasOptionalSkill"):
            for s in p["d"].get("_links", {}).get(rel, []):
                competencias.setdefault(s["uri"], None)
    for i, uri in enumerate(competencias, 1):
        competencias[uri] = pedir("skill", uri)
        if i % 100 == 0:
            print(f"  {i}/{len(competencias)} competências", flush=True)

    SAIDA.mkdir(exist_ok=True)
    with open(SAIDA / "esco-profissoes.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["profissao", "grupo_isco", "nome_grupo", "codigo", "uri", "descricao", "sinonimos"])
        for uri, p in sorted(profissoes.items(), key=lambda x: (x[1]["grupo"], x[1]["d"].get("title", ""))):
            d = p["d"]
            w.writerow([d.get("title", ""), p["grupo"], p["nome_grupo"], d.get("code", ""), uri,
                        " ".join(texto_pt(d, "description").split()), texto_pt(d, "alternativeLabel")])
    linhas = []
    for uri, p in profissoes.items():
        for rel, nome_rel in (("hasEssentialSkill", "essencial"), ("hasOptionalSkill", "opcional")):
            for s in p["d"].get("_links", {}).get(rel, []):
                c = competencias.get(s["uri"]) or {}
                linhas.append([p["d"].get("title", ""), nome_rel, s.get("title", ""),
                               "; ".join(titulos(c, "hasSkillType")), "; ".join(titulos(c, "hasReuseLevel")),
                               "; ".join(titulos(c, "broaderHierarchyConcept") or titulos(c, "broaderSkill")),
                               s["uri"]])
    linhas.sort(key=lambda x: (x[0], x[1], x[2]))
    with open(SAIDA / "esco-competencias.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["profissao", "relacao", "competencia", "tipo", "nivel_reutilizacao", "grupo", "uri"])
        w.writerows(linhas)

    # Competências transversais (as "soft skills") das profissões jurídicas, por grupo.
    trans = collections.defaultdict(lambda: collections.defaultdict(set))
    for l in linhas:
        if "transversa" in l[4].lower():
            trans[l[5] or "(sem grupo)"][l[2]].add(f"{l[0].split('/')[0]} ({l[1]})")
    hoje = dt.date.today().isoformat()
    ls = ["# Competências transversais nas profissões jurídicas (ESCO)", "",
          f"Gerado por `python3 ferramentas/esco.py` em {hoje}. Fonte: ESCO, classificação europeia de competências e "
          "profissões (© União Europeia, CC BY 4.0, https://esco.ec.europa.eu). Não é texto legal.", "",
          f"{len(profissoes)} profissões dos grupos ISCO {', '.join(g[1:] for g in GRUPOS)} "
          f"(ver `esco-profissoes.tsv`) e {len(linhas)} ligações profissão–competência (ver `esco-competencias.tsv`). "
          "Aqui ficam só as competências que a ESCO classifica como transversais (\"Aptidões e competências "
          "transversais\"), agrupadas pelo conceito mais largo da hierarquia ESCO, com as profissões em que aparecem.", ""]
    for grupo in sorted(trans):
        ls += [f"## {grupo}", ""]
        for comp in sorted(trans[grupo]):
            profs = sorted(trans[grupo][comp])
            ls.append(f"- **{comp}** — {', '.join(profs[:8])}{' …' if len(profs) > 8 else ''}")
        ls.append("")
    (SAIDA / "esco-transversais.md").write_text("\n".join(ls), encoding="utf-8")
    print(f"{len(profissoes)} profissões, {len(competencias)} competências, {len(linhas)} ligações")


if __name__ == "__main__":
    main()
