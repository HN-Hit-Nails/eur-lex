# Direito da UE e de Portugal em Markdown, preparado para agentes de IA

## O que é

Um repositório com **toda a legislação da União Europeia em vigor, em português** (65 085 actos), as
**leis portuguesas que transpõem as principais diretivas** (253 diplomas) e o **Código do IVA**, os
**acórdãos do Tribunal de Justiça** que interpretam os actos mais usados (1 353), as **orientações da
Comissão Europeia e do Comité Europeu para a Proteção de Dados** (2 805 + 81), a regulação da **Ordem dos
Advogados** e dados sobre **competências profissionais**. Tudo em texto simples (Markdown), com
índices e uma ferramenta de pesquisa que vai directa ao artigo certo, para que um agente de IA (ou uma
pessoa) consiga encontrar, ler e citar a regra exacta gastando pouco.

Vem das fontes oficiais: EUR-Lex/Cellar (Serviço das Publicações da UE), Diário da República
Eletrónico, Portal das Finanças (AT), CEPD/EDPB, portal da Ordem dos Advogados e classificação europeia ESCO. Actualiza-se sozinho todas as
segundas-feiras.

## Para que serve

- **Responder a perguntas** sobre o que a lei exige a um negócio, produto, app ou contrato — com o acto,
  o artigo e o ficheiro de onde vem a resposta. Exemplo: "que prazo tem um cliente para devolver uma
  compra online?" → Diretiva 2011/83/UE, artigo 9.º, e a lei portuguesa que a transpõe (Decreto-Lei
  n.º 24/2014).
- **Construir assistentes, bots e aplicações** que respondem com base no texto legal e não na memória
  do modelo.
- **Preparar listas de conformidade** (lançar um produto, abrir uma loja online, usar IA na empresa),
  com a origem de cada obrigação.
- **Pesquisa jurídica** de primeira linha: encontrar os actos aplicáveis, as leis de transposição, os
  acórdãos que os interpretam e as sínteses oficiais.

**Não substitui um advogado, jurista ou contabilista.** Muitas obrigações do dia a dia de uma empresa em
Portugal (impostos, segurança social, licenças, taxas de IVA) estão em lei nacional que não está aqui —
ver "O que não está aqui". Para decisões com consequências (contratos, coimas, colocação de produtos no
mercado), a leitura do agente deve ser validada por um profissional.

## Começar com um agente de IA

**Claude Code**: abrir a pasta do repositório e perguntar. O agente lê sozinho o
[`CLAUDE.md`](CLAUDE.md) (como pesquisar, como citar, que limites assinalar) e tem a skill
[`consultar-legislacao`](.claude/skills/consultar-legislacao/SKILL.md), que faz ao utilizador só as
perguntas que mudam a lei aplicável (no máximo 3) antes de pesquisar.

**Outros agentes** (Cursor, Codex, Copilot, ChatGPT com acesso ao repositório…): começar com este prompt.

```text
Este repositório tem a legislação da UE e de Portugal em Markdown. Antes de responder, lê o
CLAUDE.md e o INDICE.md e segue as regras deles: usa ferramentas/procurar.py para chegar ao
artigo certo em vez de abrir ficheiros inteiros; cita sempre acto, artigo, número, versão e
ficheiro; distingue o que está no texto do que é interpretação tua; e diz no fim o que ficou por
verificar (lei nacional que não está aqui, orientações das autoridades, versões futuras).
Responde em português de Portugal.
```

### Prompts para começar

Perguntas de negócio (substituir o exemplo pelo caso real):

1. `Vendo vernizes gel e lâmpadas UV/LED para unhas numa loja online em Portugal e também para Espanha e França. Que obrigações tenho segundo a lei da UE e a portuguesa? Começa pelas que já se aplicam e cita os artigos.`
2. `Que informação tem de constar no rótulo de um verniz gel segundo o Regulamento dos Cosméticos? Lê só os artigos necessários.`
3. `Um cliente comprou na loja online e quer devolver. Que prazo tem, como se conta e que excepções há? Cita a lei portuguesa e a diretiva de origem.`
4. `A loja tem um chatbot de IA no apoio ao cliente. Que obrigações temos segundo o Regulamento IA e desde quando se aplicam?`
5. `Vamos usar ferramentas de IA na empresa. O que exige o Regulamento IA quanto à formação do pessoal (literacia em IA)?`
6. `Que dados pessoais posso usar para enviar newsletters a clientes, e que consentimento preciso? RGPD e lei portuguesa.`

Construir aplicações e processos:

7. `Desenha um bot de apoio ao cliente que responda a dúvidas sobre devoluções e garantias usando só este repositório: como pesquisa (procurar.py), como cita, e em que casos deve encaminhar para uma pessoa.`
8. `Cria uma checklist de conformidade para colocar um novo produto cosmético no mercado da UE, com o artigo de onde vem cada ponto.`
9. `Gera um ficheiro JSON com as informações pré-contratuais obrigatórias na venda online (Diretiva 2011/83/UE e Decreto-Lei n.º 24/2014), artigo a artigo, para usar numa aplicação.`

Advocacia, ética e competências:

10. `Segundo o Estatuto da Ordem dos Advogados, que regras se aplicam à publicidade de um advogado? Procura também, no índice de pareceres da Ordem, pareceres sobre o tema.`
11. `Que competências a ESCO associa à profissão de advogado? Separa as essenciais das opcionais e diz quais servem também noutras profissões.`
12. `Explica as 12 competências do ficheiro competencias/12-competencias-juristas.md e, para cada uma, a fonte legal ou oficial.`

Pesquisa e acompanhamento:

13. `Que actos da UE em vigor tratam de embalagens e resíduos de embalagens? Lista nome, CELEX e estado, sem abrir os textos.`
14. `Há alguma recomendação recente da UE sobre competências digitais? Diz o estado e o que falta confirmar.`
15. `O que mudou na legislação na última actualização automática? Lê ue/ALTERACOES.md e resume.`

Manutenção do repositório:

16. `Corre python3 ferramentas/verificar.py e explica cada aviso.`
17. `Acrescenta ao corpus curado o acto <CELEX> na área <área>, com considerandos, contexto e transposição portuguesa.`

## O que está no repositório

Números de 2026-10-10 (contados nos ficheiros; actualizados pela actualização semanal nos índices).

| Caminho | O que tem | Quantidade |
|---|---|---|
| [`INDICE.md`](INDICE.md) | **Ponto de entrada**: como navegar gastando poucos tokens, áreas do repertório, actos curados. | — |
| [`CLAUDE.md`](CLAUDE.md) | Instruções para agentes de IA: como pesquisar, citar e que limites assinalar. | — |
| `ue/<tipo>/<ano>/<CELEX>.md` | Texto integral de **toda a legislação da UE em vigor** e da já publicada para o futuro: versão consolidada mais recente já aplicável, ou o original do Jornal Oficial. Tipos: decisões, regulamentos, concentrações, acordos internacionais, tratados, diretivas, recomendações… | 65 085 actos (64 272 em vigor, 769 em vigor por confirmar, 44 futuros); 56 435 em português, 7 590 noutra língua, 1 060 sem texto no Cellar |
| `ue/<…>/<CELEX>.futuro.md` | Versão consolidada já publicada que só se aplica numa data futura. | 16 |
| [`ue/INDICE.tsv`](ue/INDICE.tsv) | Uma linha por acto de `ue/`: estado, tipo de texto, versão, ficheiro. | 65 085 linhas |
| [`ue/ALTERACOES.md`](ue/ALTERACOES.md) | O que mudou em cada actualização e o resultado da verificação automática. | — |
| [`corpus/`](corpus/INDICE.md) | 86 actos escolhidos por serem os que um negócio digital, de comércio electrónico ou de produtos encontra na prática (RGPD, Regulamento IA, DSA, consumidores, cosméticos, CLP/REACH, IVA, trabalho, marcas…), cada um com considerandos, sínteses oficiais, leis portuguesas de transposição e acórdãos do Tribunal de Justiça. | 86 actos em 10 áreas; 82 considerandos; 81 contextos; 81 sínteses |
| [`legislacao-pt/`](legislacao-pt/INDICE.md) | Leis portuguesas que Portugal comunicou como transpondo as diretivas do corpus (e algumas mais, como o Estatuto da Ordem dos Advogados), do Diário da República Eletrónico. | 253 diplomas: 111 consolidados, 123 só o original, 19 revogados (só metadados); 61 medidas não obtidas, com o motivo no índice |
| [`catalogo/`](catalogo/legislacao-em-vigor.tsv) | Catálogo de todos os actos que o Cellar marca como em vigor: título, data, tipo, área, ELI e ligação; árvore do repertório oficial em `repertorio.md`. | 64 273 actos |
| `indice/` | Índices para pesquisar sem abrir textos: um acto por linha com nome popular, temas e descritores EuroVoc (`actos.tsv`); actos por área (`temas/`); descritor → actos (`eurovoc.tsv`); sumário de cada acto com as linhas e o tamanho de cada artigo (`artigos/`). | 65 085 actos; 20 áreas; 5 360 descritores; 644 ficheiros de sumário |
| [`jurisprudencia/`](jurisprudencia/INDICE.tsv) | Texto integral, em português, dos acórdãos, despachos e conclusões de advogados-gerais do Tribunal de Justiça citados no corpus curado (os que interpretam os 86 actos), com os actos que cada um interpreta. | 1 353 documentos (58 MB); 104 citados sem texto em português |
| [`orientacoes/comissao/`](orientacoes/comissao/INDICE.tsv) | Comunicações da Comissão no JO C que explicam como aplicar as regras (orientações, guias como o Guia Azul dos produtos, enquadramentos, perguntas e respostas). Não são legislação. | 2 805 documentos (104 MB) |
| [`orientacoes/cepd/`](orientacoes/cepd/INDICE.tsv) | Diretrizes, recomendações e declarações do Comité Europeu para a Proteção de Dados sobre o RGPD (ex.: consentimento, cookies, encarregado de proteção de dados). | 92 no índice: 65 em português, 16 só em inglês, 11 só com ligação |
| [`legislacao-pt/codigo-iva.md`](legislacao-pt/codigo-iva.md) | Código do IVA (taxas, isenções, faturação, listas I e II), compilação actualizada da Autoridade Tributária. | 123 artigos |
| [`ordem-advogados/`](ordem-advogados/INDICE.md) | Regulação dos advogados em Portugal (portal.oa.pt): texto dos regulamentos e deliberações da Ordem; **índice** dos pareceres (sem o texto). | 60 regulamentos (59 com texto); 649 pareceres no índice |
| [`competencias/`](competencias/12-competencias-juristas.md) | Competências profissionais (não é texto legal): profissões jurídicas e competências da classificação europeia ESCO; 12 competências para juristas com a fonte de cada uma. | 25 profissões; 866 ligações profissão–competência |
| [`.claude/skills/consultar-legislacao/`](.claude/skills/consultar-legislacao/SKILL.md) | Skill para o Claude responder a perguntas de negócio com poucas perguntas e poucos tokens. | — |
| `ferramentas/` | Os scripts (ver abaixo). | 17 ficheiros |
| [`.github/workflows/actualizar.yml`](.github/workflows/actualizar.yml) | Actualização automática semanal. | — |

Tamanho: cerca de 2,2 GB de ficheiros (2,06 GB em `ue/`); cerca de 0,5 GB no GitHub, comprimido.

## Como pesquisar

```bash
python3 ferramentas/procurar.py actos rgpd                       # → 32016R0679 · RGPD · 99 art. · ≈52 000 tokens
python3 ferramentas/procurar.py artigos 32011L0083 retratação    # → Artigo 9.º — Direito de retractação [≈735 tokens]
python3 ferramentas/procurar.py ler 32011L0083 9                 # só esse artigo
python3 ferramentas/procurar.py texto "prazo para devolver compra online"   # artigos mais relevantes de toda a legislação
python3 ferramentas/procurar.py pt 32011L0083                    # leis portuguesas: … Decreto-Lei n.º 24/2014 …
python3 ferramentas/procurar.py artigos lei-145-2015 segredo     # Estatuto da Ordem: Artigo 92.º — Segredo profissional
python3 ferramentas/procurar.py juris 32016R0679                 # acórdãos que interpretam o RGPD (71), mais recentes primeiro
python3 ferramentas/procurar.py texto "consentimento cookies" --fonte orientacoes   # orientações do CEPD e da Comissão
python3 ferramentas/procurar.py artigos codigo-iva taxas         # Código do IVA: Artigo 18.º — Taxas do imposto
```

Um regulamento inteiro pode ter 50 000+ tokens; o artigo que responde tem 200–2 000. A pesquisa por
relevância (`texto`) usa um índice local construído na 1.ª vez (`.cache/procurar.sqlite`, fora do git).
Sem agente de IA, também se pode navegar pelos índices no GitHub ou usar `rg` (ripgrep) nas pastas.

## Estado dos actos

Cada ficheiro começa com metadados (`estado`, `texto`, versão, `url_eurlex`, `obtido_em`…):

- `em vigor` — o Cellar marca o acto como em vigor.
- `em vigor (por confirmar)` — pelas datas já está em vigor, mas o Cellar não o marca (acabou de entrar em
  vigor, ou é uma recomendação: desde 2017 o Cellar quase não marca recomendações). O motivo está em
  `nota_estado`; confirmar no EUR-Lex.
- `futuro` — publicado, mas só entra em vigor na data indicada.

Os textos consolidados não têm valor jurídico (aviso oficial do EUR-Lex e do DRE): fazem fé os textos
publicados no Jornal Oficial e no Diário da República.

## Actualização automática

`.github/workflows/actualizar.yml` corre todas as segundas-feiras (04:23 UTC) no GitHub Actions:
refaz o catálogo, descarrega só os actos novos ou com nova versão, retira os que deixaram de vigorar
(só com prova no Cellar: data de fim de validade passada, ou marca "não em vigor" há mais de um ano), actualiza as leis portuguesas, o corpus
curado, o Código do IVA, a jurisprudência dos actos curados e as orientações da Comissão e do CEPD, refaz os índices, verifica a coerência dos dados e faz commit. O que mudou e o resultado da
verificação ficam em `ue/ALTERACOES.md`; se houver problemas graves, a execução aparece como falhada no
GitHub. Pode ser lançada à mão em Actions → "Actualizar legislação" → Run workflow.

Não estão na actualização semanal (correm à mão): a Ordem dos Advogados (`oa.py`) e a ESCO (`esco.py`).

## Ferramentas

| Script | Para quê |
|---|---|
| `procurar.py` | Pesquisa: actos, sumário de artigos, ler um artigo, texto livre, lei portuguesa de transposição. |
| `eurlex.py` | Descarrega e converte actos do Cellar; corpus curado (`nucleo`), catálogo, acto avulso (`obter <CELEX>`). |
| `completo.py` | Toda a legislação em vigor em `ue/` (listas, descarga, conversão, actualização incremental). |
| `dre.py`, `dre.js` | Leis portuguesas do Diário da República Eletrónico (precisa de Node e Playwright). |
| `indexar.py` | Índices (`indice/`, `INDICE.md`). |
| `verificar.py` | Verificação de coerência dos dados. |
| `oa.py` | Ordem dos Advogados: regulamentos e índice de pareceres. |
| `esco.py` | Competências das profissões jurídicas (ESCO). |
| `arquivo.py` | Colecções do Cellar além de `ue/`: jurisprudência, orientações da Comissão (JO C), legislação que já não está em vigor, propostas. |
| `cepd.py` | Orientações do CEPD/EDPB. |
| `at_codigos.py` | Código do IVA a partir do Portal das Finanças. |
| `nucleo.yaml` | Lista dos 86 actos curados. |
| `dre_extra.yaml` | Leis portuguesas acrescentadas além das de transposição (com a fonte). |
| `ue_ajustes.yaml` | Correcções manuais à lista de `ue/` quando o Cellar erra (com a fonte). |

```bash
pip install -r requirements.txt
npm install --prefix ferramentas && npx --prefix ferramentas playwright install chromium   # só para o DRE
python3 ferramentas/eurlex.py obter 32019L2161 --area consumidores-e-vendas --curto "Omnibus"   # acrescentar um acto
python3 ferramentas/completo.py actualizar      # toda a legislação: só o que é novo ou mudou
python3 ferramentas/dre.py tudo                 # leis portuguesas
python3 ferramentas/indexar.py && python3 ferramentas/verificar.py
```

## O que não está aqui

- Legislação que já não está em vigor, propostas da Comissão e a jurisprudência que não interpreta os
  actos curados: são grandes (≈0,5 a 2 GB de texto cada) e vão para um repositório complementar
  [`eur-lex-arquivo`](https://github.com/HNFerramentasHitNails/eur-lex-arquivo) (38 995 decisões, 48 579 actos que já não estão em vigor, 16 288 propostas; obtido com `ferramentas/arquivo.py` em 2026-10-11, sem actualização automática). Trabalhos preparatórios, perguntas parlamentares e o
  resto do Jornal Oficial série C não estão.
- Lei portuguesa que não seja de transposição das diretivas do corpus, salvo o Código do IVA e as listadas
  em `ferramentas/dre_extra.yaml` (o Código das Sociedades Comerciais já está, como transposição da
  Diretiva (UE) 2017/1132); diplomas regionais.
- Orientações das autoridades portuguesas (CNPD, ASAE, AT, Infarmed…) e as que a Comissão só publica nos
  seus sites; normas técnicas (EN, ISO), que são vendidas e protegidas (em `ue/` estão as decisões que
  publicam as referências das normas harmonizadas).
- Texto dos pareceres da Ordem dos Advogados (só o índice, com ligações).
- Bases de dados jurídicas comerciais (ex.: BDJUR da Almedina): conteúdo pago e protegido.

## Fontes e licenças

**Direito da UE** — EUR-Lex, © União Europeia, 1998-2026 (https://eur-lex.europa.eu), obtido através do
Cellar. Os documentos jurídicos podem ser reutilizados para fins comerciais ou não comerciais (Decisão
2011/833/UE); os textos consolidados e as sínteses estão sob licença
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), e os metadados em CC0. Alterações feitas:
conversão de HTML para Markdown, separação do preâmbulo, remoção de formatação tipográfica, e acrescento
de metadados e listas (transposição, jurisprudência) obtidas do Cellar.

**Legislação portuguesa** — Diário da República Eletrónico, gerido pela Imprensa Nacional-Casa da
Moeda (INCM), https://diariodarepublica.pt. O acesso universal e gratuito "compreende a possibilidade de
impressão, arquivo, pesquisa e livre acesso ao conteúdo dos atos publicados"; os textos consolidados são
produzidos pela INCM "ainda que sem valor legal". O Código do Direito de Autor (Decreto-Lei n.º 63/85,
artigo 8.º, n.º 1) exclui de protecção os textos das leis, mas as "compilações sistemáticas ou anotadas"
são obras protegidas (artigo 3.º, n.º 1, alínea c)) e o DRE indica "INCM, SA — todos os direitos
reservados". As consolidações do DRE foram incluídas neste repositório público por decisão do titular do
repositório (2026-10-09), conhecendo esta questão; se a INCM o pedir, retiram-se e ficam só os textos
originais. Alterações feitas: conversão para Markdown, remoção de ligações internas, acrescento de
metadados.

**Ordem dos Advogados** — portal.oa.pt, "© 2016, Ordem dos Advogados. Todos os direitos reservados".
Incluídos os regulamentos e deliberações (actos oficiais, tal como publicados); dos pareceres, só o
índice com ligações.

**Autoridade Tributária e Aduaneira** — Código do IVA tal como publicado no Portal das Finanças
(info.portaldasfinancas.gov.pt): compilação actualizada, sem valor oficial (faz fé o Diário da República).
Obtido aí porque a consolidação do DRE não está acessível pelo identificador ELI. Não foi encontrado aviso
de direitos no portal (não verificado em detalhe); aplica-se a mesma questão das consolidações do DRE.

**CEPD / EDPB** — "The reuse of any information of this website is authorized for commercial and
non-commercial purposes", com indicação da fonte e sem distorcer o sentido (edpb.europa.eu/copyright_en).
As diretrizes do antigo Grupo do Artigo 29.º assumidas pelo CEPD vêm do site da Comissão Europeia.

**ESCO** — classificação europeia de competências e profissões, © União Europeia, licença CC BY 4.0
(aviso legal da Comissão Europeia), https://esco.ec.europa.eu.
