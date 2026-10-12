---
titulo: "Orientações 2/2023 sobre o âmbito de aplicação técnica do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica"
titulo_en: "Guidelines 2/2023 on Technical Scope of Art. 5(3) of ePrivacy Directive"
tipo: Diretrizes
autor: Comité Europeu para a Proteção de Dados (CEPD / EDPB)
data: '2024-10-16'
lingua: português
pagina: https://www.edpb.europa.eu/documents/guideline/guidelines-22023-on-technical-scope-of-art-53-of-eprivacy-directive_en
pdf: https://www.edpb.europa.eu/system/files/documents/2025-02/edpb_guidelines_202302_technical_scope_art_53_eprivacydirective_v2_pt.pdf
obtido_em: '2026-10-12'
fonte: © Comité Europeu para a Proteção de Dados — reutilização autorizada com indicação da fonte (edpb.europa.eu/copyright_en)
---

# Orientações 2/2023 sobre o âmbito de aplicação técnica do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica

**Não é legislação:** orientação do CEPD sobre a aplicação do RGPD (ou de legislação conexa). Não vincula os tribunais, mas as autoridades de proteção de dados (em Portugal, a CNPD) seguem-na. Texto extraído automaticamente do PDF: quebras de linha e tabelas podem estar desalinhadas.
## Texto

```text
Orientações 2/2023 sobre o âmbito de
 aplicação técnica do artigo 5.º, n.º 3,
  da Diretiva Privacidade Eletrónica

                        Versão 2.0

      Adotadas em 7 de outubro de 2024
               Translations proofread by EDPB Members.

            This language version has not yet been proofread.




Adotadas                                                        1

Histórico de versões
 Versão 1.0    14 de novembro de   Adoção das Orientações para consulta pública
               2023
 Versão 2.0    7 de outubro de     Adoção das Orientações após consulta pública
               2024




Adotadas                                                                          2

Síntese

Nas presentes orientações, o CEPD aborda a aplicabilidade do artigo 5.º, n.º 3, da Diretiva Privacidade
Eletrónica a diferentes soluções técnicas. As presentes orientações complementam o Parecer 9/2014
do Grupo do Artigo 29.º sobre a aplicação da Diretiva Privacidade Eletrónica à identificação de
dispositivos e visam proporcionar uma compreensão clara das operações técnicas abrangidas pelo
artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.

O aparecimento de novos métodos de rastreio para substituir as ferramentas de rastreio existentes
[por exemplo, os testemunhos de conexão (cookies), devido à interrupção do suporte de testemunhos
de conexão (cookies) de terceiros por alguns fornecedores de programas de navegação] e para criar
novos modelos de negócio tornou-se uma preocupação fundamental no âmbito da proteção de dados.
Embora a aplicabilidade do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica esteja bem estabelecida
e executada no que diz respeito a algumas tecnologias de rastreio, tais como os testemunhos de
conexão (cookies), é necessário abordar ambiguidades relacionadas com a aplicação da referida
disposição às novas ferramentas de rastreio.

As Orientações identificam três elementos essenciais para a aplicabilidade do artigo 5.º, n.º 3, da
Diretiva Privacidade Eletrónica (secção 2.1), nomeadamente «informação», «equipamento terminal
de um assinante ou utilizador», bem como «obtenção de acesso» e «armazenamento de informações
e informações armazenadas». As Orientações preveem ainda uma análise pormenorizada de cada
elemento (secções 2.2 a 2.6).

Na secção 3, a referida análise é aplicada a uma lista não exaustiva de casos de utilização que
representam técnicas comuns, nomeadamente:

          - Rastreio de URL e píxeis
          - Processamento local
          - Rastreio baseado apenas no IP
          - Comunicação intermitente e mediada da Internet das coisas (IdC)
          - Identificador único




Adotadas                                                                                              3

Índice

1      Introdução ........................................................................................................................................ 5
2      Análise .............................................................................................................................................. 6
    2.1    Elementos essenciais para a aplicabilidade do artigo 5.º, n.º 3, da Diretiva Privacidade
    Eletrónica ............................................................................................................................................. 6
    2.2        Conceito de «informação» – Critério A.................................................................................... 7
    2.3        Conceito de «equipamento terminal de um assinante ou utilizador» – Critério B.1 .............. 7
    2.4        Conceito de «rede de comunicações pública» – Critério B.2 .................................................. 9
    2.5        Conceito de «obtenção de acesso» – Critério C.1 ................................................................. 10
    2.6     Conceitos de «armazenamento de informações» e «informações armazenadas» –
    Critério C.2 ......................................................................................................................................... 12
3      Casos de utilização ......................................................................................................................... 12
    3.1        Rastreio de URL e píxeis ......................................................................................................... 14
    3.2        Processamento local .............................................................................................................. 15
    3.3        Rastreio baseado apenas no IP .............................................................................................. 15
    3.4        Comunicação intermitente e mediada da IdC ....................................................................... 16
    3.5        Identificador único ................................................................................................................. 16




Adotadas                                                                                                                                                     4

     O Comité Europeu para a Proteção de Dados

     Tendo em conta o artigo 70.º, n.º 1, alínea e), do Regulamento (UE) 2016/679 do Parlamento Europeu
     e do Conselho, de 27 de abril de 2016, relativo à proteção das pessoas singulares no que diz respeito
     ao tratamento de dados pessoais e à livre circulação desses dados e que revoga a Diretiva 95/46/CE (a
     seguir designado por «RGPD»),

     Tendo em conta o Acordo EEE, nomeadamente o anexo XI e o Protocolo n.º 37, com a redação que lhe
     foi dada pela Decisão n.º 154/2018 do Comité Misto do EEE, de 6 de julho de 20181,

     Tendo em conta o artigo 15.º, n.º 3, da Diretiva 2002/58/CE do Parlamento Europeu e do Conselho, de
     12 de julho de 2002, relativa ao tratamento de dados pessoais e à proteção da privacidade no setor
     das comunicações eletrónicas, com a redação que lhe foi dada pela Diretiva 2009/136/CE (a seguir
     designada por «Diretiva Privacidade Eletrónica»),

     Tendo em conta os artigos 12.º e 22.º do seu Regulamento Interno,


     ADOTOU AS SEGUINTES ORIENTAÇÕES:


     1 INTRODUÇÃO
1.   Nos termos do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica, «o armazenamento de informações
     ou a possibilidade de acesso a informações já armazenadas no equipamento terminal de um assinante
     ou utilizador» só são permitidos com base no consentimento ou na necessidade para fins específicos
     definidos no artigo em questão. Tal como recordado no considerando 24 da Diretiva Privacidade
     Eletrónica2, o objetivo da disposição em causa consiste em proteger os equipamentos terminais dos
     utilizadores, uma vez que estes constituem parte integrante da esfera privada dos utilizadores. Resulta
     da redação deste artigo que o artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica não se aplica
     exclusivamente aos testemunhos de conexão (cookies), mas também às «tecnologias análogas». No
     entanto, não existe atualmente uma lista exaustiva das operações técnicas abrangidas pelo artigo 5.º,
     n.º 3, da Diretiva Privacidade Eletrónica.

2.   O Parecer 9/2014 do Grupo do Artigo 29.º sobre a aplicação da Diretiva Privacidade Eletrónica à
     identificação de dispositivos (a seguir designado por «Parecer 9/2014 do GT29») já esclareceu que a
     identificação de dispositivos é abrangida pelo âmbito de aplicação técnica do artigo 5.º, n.º 3, da
     Diretiva Privacidade Eletrónica3; contudo, devido aos novos avanços tecnológicos, são necessárias

     1 As referências a «Estados‑Membros» no presente documento devem ser entendidas como referências a

     «Estados-Membros do EEE».
     2 «O equipamento terminal dos utilizadores de redes de comunicações eletrónicas e todas as informações

     armazenadas nesse equipamento constituem parte integrante da esfera privada dos utilizadores e devem ser
     protegidos ao abrigo da Convenção Europeia para a Proteção dos Direitos Humanos e das Liberdades
     Fundamentais. Os denominados “programas-espiões” (“spyware”), “gráficos espiões” (“web bugs”) e
     “identificadores ocultos” (“hidden identifiers”) e outros dispositivos análogos podem entrar nos terminais dos
     utilizadores sem o seu conhecimento a fim de obter acesso a informações, armazenar informações escondidas
     ou permitir a rastreabilidade das atividades do utilizador e podem constituir uma grave intrusão na privacidade
     desses utilizadores. A utilização desses dispositivos deverá ser autorizada unicamente para fins legítimos, com
     o conhecimento dos utilizadores em causa.»
     3 Parecer 9/2014 do GT29, p. 11.

     Adotadas                                                                                                      5

     orientações adicionais no que diz respeito às técnicas de rastreio atualmente observadas. O panorama
     técnico tem vindo a evoluir ao longo da última década, com a crescente utilização de identificadores
     incorporados nos sistemas operativos, bem como a criação de novas ferramentas que permitem o
     armazenamento de informações em equipamentos terminais.

3.   As ambiguidades relativas ao âmbito de aplicação do artigo 5.º, n.º 3, da Diretiva Privacidade
     Eletrónica criaram incentivos para implantar soluções alternativas de rastreio dos utilizadores da
     Internet e conduziram a uma tendência para contornar as obrigações legais previstas no artigo 5.º,
     n.º 3, da Diretiva Privacidade Eletrónica. Todas estas situações suscitam preocupações e requerem
     uma análise suplementar, a fim de complementar as anteriores orientações do CEPD.

4.   O objetivo das presentes orientações consiste em realizar uma análise técnica sobre o âmbito de
     aplicação do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica, nomeadamente para clarificar o que
     se encontra tecnicamente abrangido pela expressão «para a armazenagem de informações ou para
     obter acesso à informação armazenada no equipamento terminal de um assinante ou utilizador». As
     presentes orientações não abordam as circunstâncias em que uma operação de tratamento de dados
     pode ser abrangida pelas isenções ao requisito de consentimento previsto na Diretiva Privacidade
     Eletrónica4, uma vez que tais circunstâncias devem ser analisadas caso a caso, tendo em conta a ou as
     transposições do Estado-Membro em causa e as orientações emitidas pelas autoridades nacionais
     competentes.

5.   Uma lista não exaustiva de casos de utilização específicos será analisada na parte final das presentes
     orientações.


     2 ANÁLISE
     2.1 Elementos essenciais para a aplicabilidade do artigo 5.º, n.º 3, da Diretiva
         Privacidade Eletrónica
6.   O artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica é aplicável se:

     a. CRITÉRIO A: as operações realizadas disserem respeito a «informação». Importa notar que o termo
        utilizado não é «dados pessoais», mas «informação».

     b. Critério B: as operações realizadas envolverem um «equipamento terminal» de um assinante ou
        utilizador (B.1), o que implica a necessidade de avaliar o conceito de «rede de comunicações
        pública» (B.2).

     c. CRITÉRIO C: as operações realizadas constituírem, de facto, «armazenamento» (C.1) ou «obtenção
        de acesso» (C.2). Estes dois conceitos podem ser estudados de forma independente, tal como
        recordado no Parecer 9/2014 do GT29: «A utilização da expressão “armazenadas ou objeto de
        acesso” indica que o armazenamento e o acesso não têm de ocorrer na mesma comunicação e não
        têm de ser efetuados pela mesma parte»5.




     4 Nos termos do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica: «Tal não impede o armazenamento técnico

     ou o acesso que tenha como única finalidade efetuar a transmissão de uma comunicação através de uma rede
     de comunicações eletrónicas, ou que seja estritamente necessário ao fornecedor para fornecer um serviço da
     sociedade da informação que tenha sido expressamente solicitado pelo assinante ou pelo utilizador».
     5 Parecer 9/2014 do GT29, p. 8.

     Adotadas                                                                                                     6

      Por questões de legibilidade, a entidade que obtém acesso a informações armazenadas no
      equipamento terminal do utilizador será a seguir designada por «entidade com acesso».

      2.2 Conceito de «informação» – Critério A
7.    Tal como expresso no CRITÉRIO A, a presente secção especifica o que é abrangido pelo conceito de
      «informação». A escolha do termo «informação», que abrange uma categoria mais ampla do que a
      mera noção de dados pessoais, está relacionada com o âmbito de aplicação da Diretiva Privacidade
      Eletrónica.

8.    O artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica visa proteger a esfera privada dos utilizadores, tal
      como referido no seu considerando 24: «O equipamento terminal dos utilizadores de redes de
      comunicações eletrónicas e todas as informações armazenadas nesse equipamento constituem parte
      integrante da esfera privada dos utilizadores e devem ser protegidos ao abrigo da Convenção Europeia
      para a Proteção dos Direitos Humanos e das Liberdades Fundamentais». A esfera privada é igualmente
      protegida pelo artigo 7.º da Carta dos Direitos Fundamentais da União Europeia.

9.    Com efeito, os cenários que se intrometem nesta esfera privada, mesmo sem envolver quaisquer
      dados pessoais, são explicitamente abrangidos pela redação do artigo 5.º, n.º 3, e do considerando 24
      da Diretiva Privacidade Eletrónica, por exemplo, o armazenamento de vírus no equipamento terminal
      do utilizador. Tal demonstra que a definição do termo «informação» não se deve limitar à
      particularidade de estar relacionada com uma pessoa singular identificada ou identificável.

10.   Este facto foi confirmado pelo Tribunal de Justiça da União Europeia: «Esta proteção aplica‑se a todas
      as informações armazenadas nesse equipamento terminal, independentemente de se tratar ou não de
      dados pessoais, e destina‑se, nomeadamente, como resulta desse mesmo considerando, a proteger os
      utilizadores contra o risco de identificadores ocultos ou outros dispositivos análogos entrarem nos
      terminais desses utilizadores sem o seu conhecimento»6.

11.   As questões sobre se a origem destas informações e as razões pelas quais são armazenadas no
      equipamento terminal devem ser tidas em conta na avaliação da aplicabilidade do artigo 5.º, n.º 3, da
      Diretiva Privacidade Eletrónica foram previamente clarificadas. Por exemplo, no Parecer 9/2014 do
      GT29: «Não é correto interpretar este caso como um exemplo em que o terceiro não precisa de
      consentimento para aceder a estas informações, simplesmente porque não foi ele quem as armazenou.
      A obrigatoriedade de consentimento também se aplica sempre que um valor só de leitura é acedido
      (por exemplo, solicitar o endereço MAC de uma interface de rede através da API do sistema
      operativo)»7.

12.   Em conclusão, o conceito de «informação» inclui tanto os dados não pessoais como os dados pessoais,
      independentemente de como esses dados foram armazenados e por quem, ou seja, se por uma
      entidade externa (incluindo também outras entidades que não a que tem acesso), pelo utilizador, por
      um fabricante, ou em qualquer outro cenário.

      2.3 Conceito de «equipamento terminal de um assinante ou utilizador» – Critério B.1
13.   A presente secção baseia-se na definição utilizada na Diretiva 2008/63/CE e conforme referida no
      artigo 2.º da Diretiva (UE) 2018/1972, em que o «equipamento terminal» é definido como: «[q]ualquer
      equipamento ligado direta ou indiretamente ao interface de uma rede pública de telecomunicações

      6 Acórdão do Tribunal de Justiça, de 1 de outubro de 2019, Planet 49, processo C-673/17, ECLI:EU:C:2019:801,

      n.º 70.
      7 Parecer 9/2014 do GT29, p. 8.

      Adotadas                                                                                                  7

      para transmitir, tratar ou receber informações; em ambos os casos, de ligação direta ou indireta, a
      ligação pode ser feita por cabo, fibra ótica ou por via eletromagnética; a conexão é indireta caso haja
      um aparelho intermédio entre o equipamento terminal e o interface da rede pública»8.

14.   O considerando 24 da Diretiva Privacidade Eletrónica permite uma compreensão clara do papel do
      equipamento terminal na proteção oferecida pelo artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.
      A Diretiva Privacidade Eletrónica protege a privacidade dos utilizadores não só em relação à
      confidencialidade das suas informações, mas também através da salvaguarda da integridade do
      equipamento terminal do utilizador. Esta compreensão orientará a interpretação do conceito de
      «equipamento terminal» ao longo das presentes orientações.

15.   O artigo 3.º da Diretiva Privacidade Eletrónica estabelece que, para que a Diretiva Privacidade
      Eletrónica seja aplicável, o tratamento de dados pessoais tem de ser efetuado no contexto da
      prestação de serviços de comunicações eletrónicas publicamente disponíveis nas redes de
      comunicações públicas. Tal implica que um dispositivo deve poder ser utilizado no contexto desse
      serviço e que, para ser classificado como equipamento terminal, deve estar ligado ou poder ser ligado9
      à interface de uma rede de comunicações pública. O CEPD observa que as alterações introduzidas em
      200910 no texto do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica alargaram a proteção dos
      equipamentos terminais suprimindo a referência à «utilização de redes de comunicações eletrónicas»
      como meio para armazenar informações ou obter acesso à informação armazenada no equipamento
      terminal. Por conseguinte, desde que um dispositivo disponha de uma interface de rede que o torne
      elegível para ligação (mesmo que essa ligação não exista), o artigo 5.º, n.º 3, da Diretiva Privacidade
      Eletrónica é aplicável a todas as entidades que possam armazenar e obter acesso a informações já
      armazenadas no equipamento terminal, independentemente do meio de acesso ao equipamento
      terminal e de este estar ligado ou desligado de uma rede.

16.   Os equipamentos que fazem parte da própria rede de comunicações eletrónicas pública não seriam
      considerados equipamentos terminais nos termos do artigo 5.º, n.º 3, da Diretiva Privacidade
      Eletrónica11.

17.   Um equipamento terminal pode ser composto por um variado número de peças individuais de
      hardware, que, em conjunto, formam o equipamento terminal. Este pode ou não assumir a forma de
      um dispositivo fisicamente fechado que aloja todo o hardware de visualização, processamento,
      armazenamento e periférico (por exemplo, telemóveis inteligentes, computadores portáteis,
      dispositivos de armazenamento ligados à rede, automóveis ou televisores ligados, óculos inteligentes).

18.   A Diretiva Privacidade Eletrónica reconhece que a proteção da confidencialidade das informações
      armazenadas no equipamento terminal do utilizador e da integridade do equipamento terminal do
      utilizador não se limita à proteção da esfera privada das pessoas singulares, abrangendo também o

      8  Diretiva 2008/63/CE da Comissão, de 20 de junho de 2008, relativa à concorrência nos mercados de
      equipamentos terminais de telecomunicações (Versão codificada), artigo 1.º, n.º 1.
      9 Ou seja, ter as capacidades técnicas necessárias para estar ligado à rede, mesmo que essa ligação não exista

      atualmente.
      10 Diretiva 2009/136/CE do Parlamento Europeu e do Conselho, de 25 de novembro de 2009, que altera a

      Diretiva 2002/22/CE relativa ao serviço universal e aos direitos dos utilizadores em matéria de redes e serviços
      de comunicações eletrónicas, a Diretiva 2002/58/CE relativa ao tratamento de dados pessoais e à proteção da
      privacidade no setor das comunicações eletrónicas e o Regulamento (CE) n.º 2006/2004 relativo à cooperação
      entre as autoridades nacionais responsáveis pela aplicação da legislação de defesa do consumidor (Texto
      relevante para efeitos do EEE), JO L 337 de 18.12.2009, artigo 2.º, n.º 5, e considerando 65.
      11 Para identificar os limites da rede em diferentes contextos, consultar as orientações do ORECE sobre

      abordagens comuns para identificar o ponto terminal da rede nas diferentes topologias de rede [BoR (20) 46].
      Adotadas                                                                                                      8

      direito ao sigilo da sua correspondência ou os interesses legítimos das pessoas coletivas12. Como tal,
      um equipamento terminal que permita realizar esta correspondência e os interesses legítimos das
      pessoas coletivas está protegido ao abrigo do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.

19.   O utilizador ou assinante pode possuir, alugar ou de outro modo receber o equipamento terminal.
      Vários utilizadores ou assinantes podem partilhar o mesmo equipamento terminal.

20.   A Diretiva Privacidade Eletrónica assegura esta proteção do equipamento terminal associado ao
      utilizador ou assinante, não estando a mesma dependente do facto de o utilizador ter criado os meios
      de acesso (por exemplo, se iniciou a comunicação eletrónica) ou mesmo do facto de o utilizador ter
      conhecimento dos referidos meios de acesso.

      2.4 Conceito de «rede de comunicações pública» – Critério B.2
21.   Uma vez que a situação regulada pela Diretiva Privacidade Eletrónica é a relacionada com a «prestação
      de serviços de comunicações eletrónicas publicamente disponíveis nas redes públicas de comunicações
      da Comunidade»13 e a definição de um equipamento terminal menciona especificamente o conceito
      de «rede de comunicações pública», é crucial clarificar este conceito para identificar o contexto em
      que se aplica o artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.

22.   O conceito de «rede de comunicações eletrónicas» não está definido na própria Diretiva Privacidade
      Eletrónica. Tal conceito foi originalmente referido na Diretiva 2002/21/CE relativa a um quadro
      regulamentar comum para as redes e serviços de comunicações eletrónicas (diretiva-quadro)14,
      posteriormente substituída pelo artigo 2.º, n.º 1, da Diretiva (UE) 2018/1972 (Código Europeu das
      Comunicações Eletrónicas). O texto passa a ter a seguinte redação:

         «Rede de comunicações eletrónicas», os sistemas de transmissão, sejam eles baseados ou não
         em infraestruturas permanentes ou em capacidade de administração centralizada, e, se for o
         caso, os equipamentos de comutação ou encaminhamento e os demais recursos, nomeadamente
         os elementos da rede que não se encontrem ativos, que permitem o envio de sinais por cabo, por
         feixes hertzianos, por meios óticos ou por outros meios eletromagnéticos, incluindo as redes de
         satélites, as redes fixas (com comutação de circuitos ou de pacotes, incluindo a Internet) e
         móveis, os sistemas de cabos de eletricidade, na medida em que são utilizados para a
         transmissão de sinais, as redes utilizadas para a radiodifusão sonora e televisiva e as redes de
         televisão por cabo, independentemente do tipo de informação transmitida15.

23.   Esta definição é neutra no que diz respeito às tecnologias de transmissão. De acordo com esta
      definição, uma rede de comunicações eletrónicas é qualquer sistema de rede que permite a
      transmissão de sinais eletrónicos entre os seus nós, independentemente do equipamento e dos
      protocolos utilizados.

24.   O conceito de «rede de comunicações eletrónicas» ao abrigo da Diretiva 2018/1972 não depende da
      natureza pública ou privada da infraestrutura, nem da forma como a rede é implantada ou gerida

      12 Com efeito, tal como recordado no artigo 2.º, n.º 13, da Diretiva (UE) 2018/1972 do Parlamento Europeu e

      do Conselho, de 11 de dezembro de 2018, que estabelece o Código Europeu das Comunicações Eletrónicas, o
      utilizador pode ser uma pessoa singular ou coletiva.
      13 Artigo 3.º da Diretiva Privacidade Eletrónica.
      14 Diretiva 2002/21/CE do Parlamento Europeu e do Conselho, de 7 de março de 2002, relativa a um quadro

      regulamentar comum para as redes e serviços de comunicações eletrónicas (diretiva-quadro).
      15 Diretiva (UE) 2018/1972 do Parlamento Europeu e do Conselho, de 11 de dezembro de 2018, que estabelece

      o Código Europeu das Comunicações Eletrónicas (reformulação) (Texto relevante para efeitos do EEE), artigo 2.º,
      n.º 1.
      Adotadas                                                                                                      9

      («sejam eles baseados ou não em infraestruturas permanentes ou em capacidade de administração
      centralizada»16). Por conseguinte, a definição de «rede de comunicações eletrónicas», nos termos do
      artigo 2.º da Diretiva 2018/1972, é suficientemente ampla para abranger qualquer tipo de
      infraestrutura. Inclui redes geridas ou não por um operador, redes cogeridas por um grupo de
      operadores, ou mesmo redes ad hoc em que um equipamento terminal pode entrar ou sair
      dinamicamente de uma malha de outros equipamentos terminais utilizando protocolos de transmissão
      de curto alcance.

25.   Esta definição de «rede» não confere qualquer limitação no que diz respeito ao número de
      equipamentos terminais presentes na rede em qualquer momento. Alguns sistemas de ligação em
      rede baseiam-se em nós que transmitem informações de forma ad hoc a nós atualmente ligados17 e
      podem, num dado momento, ter apenas dois pares a comunicar. Tais casos estariam abrangidos pelo
      âmbito geral da Diretiva Privacidade Eletrónica, desde que o protocolo de rede permita uma maior
      inclusão dos pares.

26.   A disponibilidade pública da rede de comunicações é necessária para que o dispositivo seja
      considerado um equipamento terminal e, consequentemente, para a aplicabilidade do artigo 5.º, n.º 3,
      da Diretiva Privacidade Eletrónica. Importa notar que o facto de a rede ser disponibilizada a um
      subconjunto limitado do público (por exemplo, assinantes, pagantes ou não, sujeitos a condições de
      elegibilidade) não torna essa rede privada 18.

      2.5 Conceito de «obtenção de acesso» – Critério C.1
27.   Para enquadrar corretamente o conceito de «obtenção de acesso», é importante ter em consideração
      o âmbito de aplicação da Diretiva Privacidade Eletrónica, estabelecido no seu artigo 1.º: «garantir um
      nível equivalente de proteção dos direitos e liberdades fundamentais, nomeadamente o direito à
      privacidade, no que respeita ao tratamento de dados pessoais no setor das comunicações eletrónicas,
      e [...] garantir a livre circulação desses dados e de equipamentos e serviços de comunicações eletrónicas
      na Comunidade».

28.   Em suma, a Diretiva Privacidade Eletrónica é um instrumento jurídico que preserva a privacidade e visa
      proteger a confidencialidade das comunicações e a integridade dos dispositivos. No considerando 24
      da Diretiva Privacidade Eletrónica, esclarece-se que, no caso das pessoas singulares, o equipamento
      terminal do utilizador constitui parte integrante da sua esfera privada e que o acesso a informações
      armazenadas no mesmo sem o conhecimento do utilizador pode constituir uma grave intrusão na sua
      privacidade.

29.   As pessoas coletivas são igualmente protegidas pela Diretiva Privacidade Eletrónica 19.
      Consequentemente, o conceito de «obtenção de acesso» nos termos do artigo 5.º, n.º 3, da Diretiva
      Privacidade Eletrónica tem de ser interpretado de um modo que assegure tais direitos contra a
      violação por terceiros.



      16 Diretiva (UE) 2018/1972 do Parlamento Europeu e do Conselho, de 11 de dezembro de 2018, que estabelece

      o Código Europeu das Comunicações Eletrónicas (reformulação) (Texto relevante para efeitos do EEE), artigo 2.º,
      n.º 1.
      17 Por exemplo, no contexto de um sistema de ligação em rede tolerante a atraso que aplica «técnicas de

      armazenamento e encaminhamento», tal como o projeto de código aberto Briar.
      18 Para uma análise mais aprofundada sobre a identificação das redes de comunicações públicas, consultar as

      Orientações do ORECE sobre a aplicação do Regulamento Internet Aberta [BoR (20) 112].
      19 Considerando 26 da Diretiva Privacidade Eletrónica, ver n.º 17 supra.

      Adotadas                                                                                                    10

30.   O armazenamento de informações ou a obtenção de acesso podem ser operações independentes e
      realizadas por entidades independentes. O armazenamento de informações e o acesso a informações
      já armazenadas não precisam de estar ambos presentes para que o artigo 5.º, n.º 3, da Diretiva
      Privacidade Eletrónica seja aplicável.

31.   Conforme referido no Parecer 9/2014 do GT29: «A utilização da expressão “armazenadas ou objeto de
      acesso” indica que o armazenamento e o acesso não têm de ocorrer na mesma comunicação e não têm
      de ser efetuados pela mesma parte. As informações armazenadas por uma parte (incluindo as
      informações armazenadas pelo utilizador ou pelo fabricante do dispositivo) que são posteriormente
      objeto de acesso por uma outra parte estão, por conseguinte, abrangidas pelo âmbito de aplicação do
      artigo 5.º, n.º 3»20. Deste modo, não existem restrições quanto à origem da informação no
      equipamento terminal para que o conceito de «acesso» seja aplicável.

32.   Sempre que uma entidade tome medidas no sentido de obter acesso à informação armazenada no
      equipamento terminal, aplica-se o artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica. Normalmente,
      tal implica que a entidade com acesso envie proativamente instruções específicas para o equipamento
      terminal, a fim de receber de volta a informação específica. É o caso, por exemplo, dos testemunhos
      de conexão (cookies), em que a entidade com acesso dá instruções ao equipamento terminal para
      enviar proativamente informações em cada chamada subsequente de protocolo de transferência de
      hipertexto («HTTP»).

33.   Tal é igualmente o caso quando a entidade com acesso distribui software no equipamento terminal do
      utilizador que está armazenado e, em seguida, chama proativamente um parâmetro de interface de
      programação de aplicações (API) através da rede. Outros exemplos incluem o código JavaScript, em
      que a entidade com acesso dá instruções ao navegador do utilizador para enviar pedidos assíncronos
      com as informações específicas. Tal acesso é claramente abrangido pelo âmbito de aplicação do
      artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica, uma vez que a entidade com acesso dá instruções
      explícitas ao equipamento terminal para enviar as informações.

34.   Em determinados casos, a entidade que dá instruções ao equipamento terminal para devolver os
      dados específicos e a entidade que recebe as informações podem não ser a mesma. Tal pode resultar
      da disponibilização e/ou utilização de um mecanismo comum entre as duas entidades. Dar instruções
      ao dispositivo para enviar informações já armazenadas (por exemplo, através da utilização de um
      protocolo, ou um SDK21 que implique o envio proativo de informações pelo equipamento terminal)
      torna possível uma intrusão no equipamento terminal, pelo que esse acesso desencadeia a
      aplicabilidade do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica. Tal como referido no
      Parecer 9/2014 do GT29, este pode ser o caso quando um sítio Web dá instruções ao equipamento
      terminal para enviar informações a serviços de publicidade de terceiros através da inclusão de um píxel
      de rastreio22. Este caso de utilização é desenvolvido na secção 3.1.




      20 Parecer 9/2014 do GT29, p. 8.
      21 Um SDK (software development kit, «conjunto de desenvolvimento de software») é um conjunto de

      ferramentas de desenvolvimento de software disponibilizadas para facilitar a criação de software de
      aplicações.
      22 Parecer 9/2014 do GT29, p. 9.

      Adotadas                                                                                              11

      2.6 Conceitos de «armazenamento de informações» e «informações armazenadas»
          – Critério C.2
35.   O armazenamento de informações na aceção do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica
      refere-se à colocação de informações num suporte físico de armazenamento eletrónico que constitui
      parte integrante do equipamento terminal de um utilizador ou assinante23.

36.   Geralmente, as informações não são armazenadas no equipamento terminal de um utilizador ou
      assinante através do acesso direto à memória do dispositivo por outra parte, mas sim através da
      instrução de software no equipamento terminal para gerar informações específicas. Considera-se que
      o armazenamento efetuado através de tais instruções é iniciado diretamente pela outra parte. Tal
      inclui a utilização de protocolos estabelecidos, como o armazenamento de testemunhos de conexão
      (cookies) do navegador, bem como de software personalizado, independentemente de quem criou ou
      instalou os protocolos ou o software no equipamento terminal.

37.   A Diretiva Privacidade Eletrónica não estabelece qualquer limite máximo ou mínimo para o período de
      tempo que a informação deve persistir num suporte de armazenamento para ser considerada como
      armazenada, nem existe um limite máximo ou mínimo para a quantidade de informação a armazenar.

38.   Do mesmo modo, o conceito de «armazenamento» não depende do tipo de suporte em que a
      informação é armazenada. Exemplos típicos incluem discos rígidos («HDD»), unidades de estado sólido
      («SSD»), memórias de leitura programáveis apagáveis eletricamente («EEPROM») e memórias de
      acesso aleatório («RAM»), mas não são excluídos do âmbito de aplicação cenários menos típicos que
      envolvam um suporte como fita magnética ou cache da unidade central de processamento («CPU»). O
      suporte de armazenamento pode ser ligado internamente (por exemplo, através de uma ligação SATA)
      ou externamente (por exemplo, através de uma ligação USB).

39.   «Informações armazenadas» refere-se às informações já existente no equipamento terminal,
      independentemente da origem ou da natureza de tais informações. Tal inclui qualquer resultado do
      armazenamento de informações na aceção do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica,
      conforme descrito supra (quer pela mesma parte que obteria acesso posteriormente, quer por outro
      terceiro). Inclui ainda os resultados de processos de armazenamento de informações fora do âmbito
      de aplicação do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica, tais como: armazenamento no
      equipamento terminal pelo próprio utilizador ou assinante, ou por um fabricante de hardware (como
      os endereços MAC dos controladores de interface de rede), sensores integrados no equipamento
      terminal ou processos e programas executados no equipamento terminal, que podem ou não produzir
      informações que dependem ou derivam das informações armazenadas.


      3 CASOS DE UTILIZAÇÃO
40.   Tal como salientado na introdução das presentes orientações24, estas não analisam a aplicação das
      isenções à obrigação de obter o consentimento prevista no artigo 5.º, n.º 3, da Diretiva Privacidade
      Eletrónica. O CEPD recorda que, em todos os casos em que exista armazenamento de informações ou
      obtenção de acesso a informações já armazenadas, teria de ser avaliado se é necessário consentimento
      ou se poderia ser aplicável uma isenção nos termos do artigo 5.º, n.º 3, da Diretiva Privacidade



      23 Tal como definido na secção 2.3 das presentes orientações.
      24 Ver n.º 4 supra.

      Adotadas                                                                                         12

      Eletrónica. O leitor deve, portanto, considerar as isenções no seu caso de utilização, em conjunto com
      esta análise técnica.

41.   Sem prejuízo do contexto específico em que as categorias técnicas necessárias podem ser utilizadas
      para determinar se o artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica é aplicável, é possível
      identificar, de forma não exaustiva, categorias abrangentes de identificadores e informações que são
      amplamente utilizadas e que podem estar sujeitas à aplicabilidade do artigo 5.º, n.º 3, da Diretiva
      Privacidade Eletrónica.

42.   A comunicação em rede baseia-se normalmente num modelo estratificado que exige a utilização de
      identificadores para permitir o estabelecimento e a realização corretos da comunicação. A
      comunicação dos identificadores em causa a atores remotos é efetuada através de software, seguindo
      protocolos de comunicação acordados. Tal como acima referido, o facto de a entidade recetora poder
      não ser a entidade que dá instruções para o envio da informação não exclui a aplicação do artigo 5.º,
      n.º 3, da Diretiva Privacidade Eletrónica. Tal pode dizer respeito a identificadores de encaminhamento,
      como o endereço MAC ou IP do equipamento terminal, mas também a identificadores de sessão (SSRC,
      identificador Websocket) ou a fichas de autenticação.

43.   Do mesmo modo, o protocolo de aplicação pode incluir vários mecanismos para fornecer dados de
      contexto (como o cabeçalho HTTP, incluindo o campo «accept» ou o agente do utilizador), um
      mecanismo de armazenamento temporário (caching) (como ETag25) ou outras funcionalidades [sendo
      os testemunhos de conexão (cookies) uma delas, ou HSTS26]. Mais uma vez, o recurso a tais
      mecanismos para recolher informações (por exemplo, no contexto da identificação de dispositivos 27
      ou do rastreio de identificadores de recursos) pode conduzir à aplicação do artigo 5.º, n.º 3, da Diretiva
      Privacidade Eletrónica.

44.   Por outro lado, existem alguns contextos em que as aplicações locais instaladas no equipamento
      terminal utilizam algumas informações estritamente dentro do terminal, como pode ser o caso das API
      do sistema dos telemóveis inteligentes (acesso à câmara, microfone, sensor GPS, chip acelerador, chip
      de rádio, acesso a ficheiros locais, lista de contactos, acesso a identificadores, etc.). Este pode ser
      também o caso dos navegadores Web que processam informações armazenadas ou geradas dentro
      do dispositivo [tais como testemunhos de conexão (cookies), armazenamento local, WebSQL ou
      mesmo informações fornecidas pelos próprios utilizadores]. Desde que as informações não saiam do
      dispositivo, a utilização dessas informações por uma aplicação não constituiria uma «obtenção de
      acesso a informações já armazenadas» na aceção do artigo 5.º, n.º 3, da Diretiva Privacidade
      Eletrónica, mas quando tais informações ou qualquer derivação de tais informações forem acedidas,
      seria aplicável o artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.

45.   Por último, em determinados casos, elementos de software malicioso são distribuídos por atores (por
      exemplo, software de mineração criptográfica ou software malicioso no sentido geral) que exploram
      as capacidades de processamento do equipamento terminal em benefício do ator de distribuição. A
      distribuição do referido software malicioso no equipamento terminal do utilizador constituiria um
      «armazenamento» na aceção do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica. Além disso, caso



      25 O HTTP ETag é um identificador que permite efetuar um pedido condicional com base na validade dos dados

      do cliente armazenados em cache.
      26 O HTTP Strict Transport Security (HSTS) permite que os servidores especifiquem quais os recursos que devem

      ser sempre solicitados utilizando ligações HTTPS.
      27 Tal como referido na introdução, consultar o Parecer 9/2014 do Grupo do Artigo 29.º sobre a aplicação da

      Diretiva Privacidade Eletrónica à identificação de dispositivos.
      Adotadas                                                                                                  13

      o software estabeleça uma ligação à rede para enviar informações numa fase posterior, tal constituiria
      uma «obtenção de acesso» na aceção do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.

46.   Para um subconjunto destas categorias que apresentam um interesse específico, quer devido à sua
      utilização generalizada, quer porque se justifica um estudo específico no que diz respeito às
      circunstâncias da sua utilização, apresenta-se a seguir uma análise específica.

      3.1 Rastreio de URL e píxeis
47.   Um píxel de rastreio é uma hiperligação para um recurso, normalmente um ficheiro de imagem,
      incorporada num elemento de conteúdo como um sítio Web ou uma mensagem de correio eletrónico.
      Este píxel geralmente não cumpre qualquer finalidade relacionada com o conteúdo solicitado
      propriamente dito; a sua única finalidade é estabelecer automaticamente uma comunicação do cliente
      ao anfitrião do píxel, que, de outro modo, não teria ocorrido. No entanto, tal não é sistemático e os
      píxeis de rastreio também podem ser criados acrescentando informações adicionais às imagens de
      carregamento de hiperligações que sejam relevantes para o conteúdo apresentado ao utilizador. O
      estabelecimento da comunicação transmite várias informações ao anfitrião do píxel, consoante o caso
      de utilização específico.

48.   No caso de uma mensagem de correio eletrónico, o remetente pode incluir um píxel de rastreio para
      detetar quando o destinatário lê a mensagem de correio eletrónico. Os píxeis de rastreio em sítios
      Web podem estabelecer uma ligação a uma entidade que recolhe muitos desses pedidos e que, por
      conseguinte, pode rastrear o comportamento dos utilizadores. Os píxeis de rastreio em causa podem
      também conter identificadores, metadados ou conteúdos adicionais como parte da ligação. Estes
      dados podem ser adicionados pelo proprietário do sítio Web, possivelmente relacionados com a
      atividade do utilizador no sítio Web em causa, de modo que possam ser gerados relatórios analíticos
      de utilização. Podem ser igualmente gerados dinamicamente através da lógica de aplicação do lado do
      cliente fornecida pela entidade.

49.   As ligações de rastreio podem funcionar da mesma forma; contudo, o identificador é anexado ao
      endereço do sítio Web. Quando o localizador uniforme de recursos («URL») é visitado pelo utilizador,
      o sítio Web visado carrega o recurso solicitado, mas recolhe também um identificador que não é
      relevante em termos de identificação do recurso. São muito frequentemente utilizados pelos sítios
      Web de comércio eletrónico para identificar a origem da sua fonte de tráfego de entrada. Por exemplo,
      tais sítios Web podem fornecer ligações rastreadas a parceiros para serem utilizadas no seu domínio,
      de modo que o sítio Web de comércio eletrónico saiba qual dos seus parceiros é responsável por uma
      venda e pague uma comissão, uma prática conhecida como marketing de afiliados.

50.   Tanto as ligações de rastreio como os píxeis de rastreio podem ser distribuídos através de uma grande
      variedade de canais, por exemplo, através de mensagens de correio eletrónico, sítios Web ou mesmo,
      no caso das ligações de rastreio, através de qualquer tipo de sistema de mensagens de texto. Essa
      distribuição ao equipamento terminal do utilizador constitui armazenamento, pelo menos através do
      mecanismo de armazenamento temporário (caching) do software do lado do cliente. Como tal, aplica-
      se o artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica, mesmo que este armazenamento não seja
      permanente.

51.   A inclusão de informações de rastreio nos URL ou imagens (píxeis) enviados ao utilizador constitui uma
      instrução dada ao equipamento terminal no sentido de devolver as informações específicas (o
      identificador especificado). No caso dos píxeis de rastreio construídos dinamicamente, é a distribuição
      da lógica de aplicação (normalmente um código JavaScript) que constitui a instrução.
      Consequentemente, pode considerar-se que a recolha de identificadores fornecida através desses
      Adotadas                                                                                             14

      mecanismos de rastreio constitui uma «obtenção de acesso» na aceção do artigo 5.º, n.º 3, da Diretiva
      Privacidade Eletrónica, pelo que também se aplica a essa etapa.

      3.2 Processamento local
52.   Algumas tecnologias baseiam-se no processamento local instruído por software distribuído no
      equipamento terminal dos utilizadores, em que a informação produzida pelo processamento local é
      posteriormente disponibilizada a atores selecionados através da API do lado do cliente. Este pode ser,
      por exemplo, o caso de uma API fornecida pelo navegador Web, em que os resultados gerados
      localmente podem ser acedidos remotamente.

53.   Se, em qualquer momento e, por exemplo, no código do lado do cliente, a informação processada for
      disponibilizada a terceiros, por exemplo, devolvida através da rede a um servidor, tal operação
      (instruída pela entidade que produz o código do lado do cliente distribuído no equipamento terminal
      do utilizador) constituiria uma «obtenção de acesso a informações já armazenadas». O facto de estas
      informações estarem a ser produzidas localmente não exclui a aplicação do artigo 5.º, n.º 3, da Diretiva
      Privacidade Eletrónica.

      3.3 Rastreio baseado apenas no IP
54.   Alguns fornecedores estão a desenvolver soluções que se baseiam apenas na recolha de um
      componente, nomeadamente o endereço IP, para rastrear a navegação28 do utilizador, em certos casos
      através de vários domínios. Nesse contexto, o artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica
      poderia ser aplicável mesmo que a instrução para disponibilizar o IP tenha sido dada por uma entidade
      diferente da entidade recetora.

55.   No entanto, a obtenção de acesso a endereços IP apenas desencadearia a aplicação do artigo 5.º, n.º 3,
      da Diretiva Privacidade Eletrónica nos casos em que as informações em causa provenham do
      equipamento terminal de um assinante ou utilizador. Embora não seja sistematicamente o caso (por
      exemplo, quando o CGNAT29 está ativado), o IPv4 estático de saída proveniente do router de um
      utilizador seria abrangido por esse caso, bem como os endereços IPv6, uma vez que são parcialmente
      definidos pelo anfitrião. A menos que a entidade possa assegurar que o endereço IP não provém do
      equipamento terminal de um utilizador ou assinante, deverá tomar todas as medidas nos termos do
      artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.

56.   Embora as presentes orientações não analisem a aplicação das isenções à obrigação de obter o
      consentimento prevista no artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica, é importante recordar
      mais uma vez que a aplicabilidade do referido artigo não significa sistematicamente que seja
      necessário obter consentimento. Por conseguinte, o CEPD recorda que, em cada caso, teria de ser
      avaliado se é necessário consentimento ou se poderia ser aplicável uma isenção nos termos do
      artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica30.




      28 Tal é adicional e independente da utilização e função de um endereço IP para o estabelecimento e

      transferência ou transmissão de comunicações técnicas subjacentes, ou do facto de poderem ou não ser dados
      pessoais (no que respeita à análise da privacidade eletrónica, trata-se de «informação»).
      29 O Carrier-Grade NAT ou CGNAT é utilizado pelos fornecedores de serviços Internet para maximizar a

      utilização de um espaço limitado de endereços IP. Agrupa um certo número de assinantes sob o mesmo
      endereço IP público.
      30 O Parecer 9/2014 do GT29 prevê alguns exemplos em que o consentimento pode não ser necessário.

      Adotadas                                                                                                15

      3.4 Comunicação intermitente e mediada da IdC
57.   Os dispositivos IdC (Internet das coisas) produzem informações continuamente ao longo do tempo,
      por exemplo, através de sensores incorporados no dispositivo, que podem ou não ser pré-processadas
      localmente. Em muitos casos, as informações são disponibilizadas a um servidor remoto, mas as
      modalidades dessa recolha podem variar.

58.   Alguns dispositivos IdC têm uma ligação direta a uma rede de comunicações pública com um cartão
      SIM celular. Outros poderão ter uma ligação indireta a uma rede de comunicações pública, por
      exemplo, através da utilização de WIFI ou da transmissão de informações para outro dispositivo
      mediante uma ligação ponto a ponto (por exemplo, através de Bluetooth). O outro dispositivo pode
      ser, por exemplo, um telemóvel inteligente ou uma porta de ligação dedicada que pode ou não pré-
      processar a informação antes de a enviar para o servidor.

59.   Os dispositivos IdC podem ser instruídos pelo fabricante para transmitir sempre a informação
      recolhida, embora continuem a guardar primeiro localmente a informação, por exemplo, até que
      esteja disponível uma ligação.

60.   Em qualquer caso, o dispositivo IdC, quando ligado (direta ou indiretamente) a uma rede de
      comunicações pública, seria ele próprio considerado um equipamento terminal. O facto de a
      informação ser transmitida em fluxo contínuo ou armazenada em cache para comunicação
      intermitente não altera a natureza dessa informação. Em ambas as situações, o artigo 5.º, n.º 3, da
      Diretiva Privacidade Eletrónica seria aplicável, uma vez que existe, através da instrução de um código
      no dispositivo IdC para enviar os dados armazenados dinamicamente para o servidor remoto, uma
      «obtenção de acesso».

      3.5 Identificador único
61.   Uma ferramenta comum utilizada pelas empresas é o conceito de «identificadores únicos» ou de
      «identificadores persistentes». Tais identificadores podem ser obtidos a partir de dados pessoais
      persistentes (nome e apelido, endereço de correio eletrónico, número de telefone, etc.) que são
      armazenados em hash no dispositivo do utilizador, recolhidos e partilhados entre vários responsáveis
      pelo tratamento de dados para identificar inequivocamente uma pessoa em diferentes conjuntos de
      dados [dados de utilização recolhidos através da utilização de um sítio Web ou de uma aplicação, dados
      de gestão das relações com os clientes (CRM) relacionados com compras ou assinaturas em linha ou
      fora de linha, etc.]. Nos sítios Web, os dados pessoais persistentes são geralmente obtidos no contexto
      da autenticação ou da assinatura de boletins informativos.

62.   Tal como referido anteriormente, o facto de as informações estarem a ser introduzidas pelo utilizador
      não exclui a aplicação do artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica no que diz respeito ao
      armazenamento, uma vez que estas informações são armazenadas temporariamente no equipamento
      terminal antes de serem recolhidas.

63.   No contexto da recolha de «identificadores únicos» em sítios Web ou aplicações móveis, a entidade
      que faz a recolha dá instruções ao navegador (através da distribuição de código do lado do cliente)
      para enviar essa informação. Como tal, está a ocorrer uma «obtenção de acesso» e aplica-se o
      artigo 5.º, n.º 3, da Diretiva Privacidade Eletrónica.




      Adotadas                                                                                            16
```
