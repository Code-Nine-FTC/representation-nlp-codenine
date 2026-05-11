"""
Catálogo de intenções (intents) reconhecidas pela busca semântica.

Cada intenção agrupa:
  - phrases: lista de frases canônicas em PT-BR. O matcher BOW compara
    a entrada do usuário contra TODAS as frases de TODAS as intents;
    a frase mais próxima por similaridade de cosseno define qual intent
    vence. Quanto mais variações de uma mesma pergunta listadas aqui,
    mais robusto fica o reconhecimento.
  - sql: a SQL a executar quando essa intent for escolhida.
  - kind: "count" para resultado escalar, "rows" para lista de linhas.
    O app usa esse campo para decidir como serializar o resultado.

Para adicionar uma nova pergunta reconhecida basta acrescentar um
dicionário a INTENTS. Não há acoplamento por índice como na versão
anterior — frases e SQL ficam no mesmo lugar.
"""

INTENTS = [
    # ===================== Contagens =====================
    {
        "phrases": [
            "quantas pessoas existem",
            "qual o total de pessoas",
            "numero de pessoas cadastradas",
            "quantas pessoas estao cadastradas",
            "total de pessoas no banco",
            "ha quantas pessoas",
            "quantos registros existem",
            "quantas pessoas tem no banco",
            "total de pessoas",
            "me diga quantas pessoas existem",
            "qual a quantidade de pessoas",
            "quantas imagens estao catalogadas",
            "quantas imagens existem",
            "total de imagens",
            "qnts pessoas existem",
            "quantas pessoas cadastradas",
            "qnts imgns estao catalogadas",
            "qntas imagens",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas brancas existem",
            "total de pessoas brancas",
            "numero de pessoas de etnia branca",
            "quantos brancos estao cadastrados",
            "quantas pessoas da etnia branca",
            "total de brancos",
            "quantos brancos existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'branca'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas negras existem",
            "total de pessoas negras",
            "numero de pessoas de etnia negra",
            "quantos negros estao cadastrados",
            "quantas pessoas da etnia negra",
            "total de negros",
            "quantos negros existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'negra'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas pardas existem",
            "total de pessoas pardas",
            "numero de pessoas de etnia parda",
            "quantos pardos estao cadastrados",
            "quantas pessoas da etnia parda",
            "total de pardos",
            "quantos pardos existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'parda'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas asiaticas existem",
            "total de pessoas asiaticas",
            "numero de pessoas de etnia asiatica",
            "quantos asiaticos estao cadastrados",
            "quantas pessoas da etnia asiatica",
            "total de asiaticos",
            "quantos asiaticos existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'asiatica'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas indigenas existem",
            "total de pessoas indigenas",
            "numero de pessoas de etnia indigena",
            "quantos indigenas estao cadastrados",
            "quantas pessoas da etnia indigena",
            "total de indigenas",
            "quantos indigenas existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'indigena'",
        "kind": "count",
    },

    # ===================== Listagem geral =====================
    {
        "phrases": [
            "mostrar todas as pessoas",
            "listar pessoas cadastradas",
            "exibir todas as pessoas",
            "mostrar pessoas",
            "listar todos",
            "exiba todos os cadastrados",
            "quem sao as pessoas cadastradas",
            "mostre todas as pessoas",
            "liste todas as pessoas",
            "quais sao as pessoas",
            "me mostre as pessoas",
            "exiba as pessoas cadastradas",
            "exibir todas as imagens",
        ],
        "sql": "SELECT * FROM people_images",
        "kind": "rows",
    },

    # ===================== Contagens por cor de cabelo =====================
    {
        "phrases": [
            "quantas pessoas tem cabelo loiro",
            "total de pessoas loiras",
            "numero de pessoas de cabelo loiro",
            "quantos loiros existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE cor_cabelo = 'loiro'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas tem cabelo preto",
            "total de pessoas de cabelo preto",
            "numero de pessoas de cabelo preto",
            "quantos de cabelo preto existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE cor_cabelo = 'preto'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas tem cabelo castanho",
            "total de pessoas de cabelo castanho",
            "numero de pessoas de cabelo castanho",
            "quantos de cabelo castanho existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE cor_cabelo = 'castanho'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas ruivas existem",
            "total de pessoas ruivas",
            "numero de pessoas de cabelo ruivo",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE cor_cabelo = 'ruivo'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas tem cabelo grisalho",
            "total de pessoas de cabelo grisalho",
            "numero de pessoas de cabelo grisalho",
            "quantos de cabelo grisalho existem",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE cor_cabelo = 'grisalho'",
        "kind": "count",
    },

    # ===================== Seleção por cor de cabelo =====================
    {
        "phrases": [
            "mostrar pessoas com cabelo loiro",
            "pessoas loiras",
            "quem tem cabelo loiro",
            "exibir pessoas de cabelo loiro",
            "listar pessoas loiras",
            "mostre quem tem cabelo loiro",
            "quais pessoas tem cabelo loiro",
            "liste as pessoas loiras",
            "exiba as pessoas de cabelo loiro",
            "me mostre as pessoas loiras",
            "pessoas de cabelo loiro",
            "cabelo loiro",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'loiro'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas com cabelo preto",
            "pessoas de cabelo preto",
            "quem tem cabelo preto",
            "listar pessoas com cabelo preto",
            "mostre quem tem cabelo preto",
            "quais pessoas tem cabelo preto",
            "liste as pessoas de cabelo preto",
            "exiba as pessoas de cabelo preto",
            "me mostre as pessoas de cabelo preto",
            "cabelo preto",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'preto'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas com cabelo castanho",
            "pessoas de cabelo castanho",
            "quem tem cabelo castanho",
            "listar pessoas com cabelo castanho",
            "mostre quem tem cabelo castanho",
            "quais pessoas tem cabelo castanho",
            "liste as pessoas de cabelo castanho",
            "exiba as pessoas de cabelo castanho",
            "me mostre as pessoas de cabelo castanho",
            "cabelo castanho",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'castanho'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas ruivas",
            "pessoas de cabelo ruivo",
            "quem tem cabelo ruivo",
            "listar pessoas ruivas",
            "mostre quem tem cabelo ruivo",
            "quais pessoas sao ruivas",
            "exiba as pessoas ruivas",
            "cabelo ruivo",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'ruivo'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas com cabelo grisalho",
            "pessoas de cabelo grisalho",
            "quem tem cabelo grisalho",
            "mostre quem tem cabelo grisalho",
            "quais pessoas tem cabelo grisalho",
            "liste as pessoas de cabelo grisalho",
            "exiba as pessoas de cabelo grisalho",
            "cabelo grisalho",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'grisalho'",
        "kind": "rows",
    },

    # ===================== Seleção por etnia =====================
    {
        "phrases": [
            "mostrar pessoas brancas",
            "pessoas de etnia branca",
            "exibir pessoas brancas",
            "listar pessoas brancas",
            "mostre as pessoas brancas",
            "quais sao as pessoas brancas",
            "liste os brancos",
            "pessoas da etnia branca",
            "brancos cadastrados",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'branca'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas negras",
            "pessoas de etnia negra",
            "exibir pessoas negras",
            "listar pessoas negras",
            "mostre as pessoas negras",
            "quais sao as pessoas negras",
            "liste os negros",
            "pessoas da etnia negra",
            "negros cadastrados",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'negra'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas pardas",
            "pessoas de etnia parda",
            "exibir pessoas pardas",
            "listar pessoas pardas",
            "mostre as pessoas pardas",
            "quais sao as pessoas pardas",
            "liste os pardos",
            "pessoas da etnia parda",
            "pardos cadastrados",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'parda'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas asiaticas",
            "pessoas de etnia asiatica",
            "exibir pessoas asiaticas",
            "listar pessoas asiaticas",
            "mostre as pessoas asiaticas",
            "quais sao as pessoas asiaticas",
            "liste os asiaticos",
            "pessoas da etnia asiatica",
            "asiaticos cadastrados",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'asiatica'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas indigenas",
            "pessoas de etnia indigena",
            "exibir pessoas indigenas",
            "listar pessoas indigenas",
            "mostre as pessoas indigenas",
            "quais sao as pessoas indigenas",
            "liste os indigenas",
            "pessoas da etnia indigena",
            "indigenas cadastrados",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'indigena'",
        "kind": "rows",
    },

    # ===================== Seleção por faixa etária =====================
    {
        "phrases": [
            "mostrar criancas pequenas",
            "bebes cadastrados",
            "pessoas de 0 a 5 anos",
            "criancas de 0 a 5 anos",
            "lista de bebes",
            "mostre os bebes",
            "criancas de 0 a 5",
            "bebes de 0 a 5 anos",
        ],
        "sql": "SELECT * FROM people_images WHERE faixa_etaria = '0-5'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar criancas",
            "criancas cadastradas",
            "pessoas de 5 a 12 anos",
            "criancas de 5 a 12 anos",
            "criancas de 5 a 12",
            "mostre as criancas",
            "criancas em idade escolar",
            "menores de 12 anos",
        ],
        "sql": "SELECT * FROM people_images WHERE faixa_etaria = '5-12'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar adolescentes",
            "adolescentes cadastrados",
            "pessoas de 13 a 17 anos",
            "listar adolescentes",
            "mostre os adolescentes",
            "jovens de 13 a 17 anos",
            "adolescentes de 13 a 17",
        ],
        "sql": "SELECT * FROM people_images WHERE faixa_etaria = '13-17'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar jovens adultos",
            "jovens cadastrados",
            "pessoas de 18 a 25 anos",
            "listar jovens",
            "mostre os jovens",
            "jovens de 18 a 25 anos",
            "pessoas jovens",
            "maiores de idade",
        ],
        "sql": "SELECT * FROM people_images WHERE faixa_etaria = '18-25'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar adultos",
            "adultos cadastrados",
            "pessoas de 26 a 40 anos",
            "listar adultos",
            "mostre os adultos",
            "adultos de 26 a 40 anos",
            "pessoas de 26 a 40",
        ],
        "sql": "SELECT * FROM people_images WHERE faixa_etaria = '26-40'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pessoas de meia idade",
            "pessoas de 41 a 60 anos",
            "listar pessoas de meia idade",
            "mostre as pessoas de meia idade",
            "adultos de 41 a 60 anos",
            "pessoas de 41 a 60",
            "meia idade",
        ],
        "sql": "SELECT * FROM people_images WHERE faixa_etaria = '41-60'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar idosos",
            "idosos cadastrados",
            "pessoas com mais de 60 anos",
            "listar idosos",
            "mostre os idosos",
            "pessoas idosas",
            "terceira idade",
            "melhor idade",
            "acima de 60 anos",
        ],
        "sql": "SELECT * FROM people_images WHERE faixa_etaria = '60+'",
        "kind": "rows",
    },

    # ===================== Contagens combinadas =====================
    {
        "phrases": [
            "quantas pessoas brancas de cabelo loiro",
            "total de brancos loiros",
            "quantos brancos tem cabelo loiro",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'branca' AND cor_cabelo = 'loiro'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas negras de cabelo preto",
            "total de negros de cabelo preto",
            "quantos negros tem cabelo preto",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'negra' AND cor_cabelo = 'preto'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantos idosos existem",
            "quantas pessoas tem mais de 60 anos",
            "total de idosos",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE faixa_etaria = '60+'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas criancas existem",
            "total de criancas",
            "quantas pessoas tem menos de 12 anos",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE faixa_etaria IN ('0-5', '5-12')",
        "kind": "count",
    },

    # ===================== Combinacoes: etnia + cor_cabelo =====================
    {
        "phrases": [
            "mostrar brancos de cabelo loiro",
            "pessoas brancas com cabelo loiro",
            "brancos loiros",
            "exiba pessoas brancas de cabelo loiro",
            "liste brancos com cabelo loiro",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'branca' AND cor_cabelo = 'loiro'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar brancos de cabelo preto",
            "pessoas brancas com cabelo preto",
            "brancos de cabelo preto",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'branca' AND cor_cabelo = 'preto'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar brancos de cabelo castanho",
            "pessoas brancas com cabelo castanho",
            "brancos de cabelo castanho",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'branca' AND cor_cabelo = 'castanho'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar brancos de cabelo grisalho",
            "pessoas brancas com cabelo grisalho",
            "brancos de cabelo grisalho",
            "idosos brancos",
            "pessoas brancas idosas",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'branca' AND cor_cabelo = 'grisalho'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar negros de cabelo preto",
            "pessoas negras com cabelo preto",
            "negros de cabelo preto",
            "mostre pessoas negras de cabelo preto",
            "liste negros com cabelo preto",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'negra' AND cor_cabelo = 'preto'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar negros de cabelo castanho",
            "pessoas negras com cabelo castanho",
            "negros de cabelo castanho",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'negra' AND cor_cabelo = 'castanho'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar asiaticos de cabelo preto",
            "pessoas asiaticas com cabelo preto",
            "asiaticos de cabelo preto",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'asiatica' AND cor_cabelo = 'preto'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar asiaticos de cabelo castanho",
            "pessoas asiaticas com cabelo castanho",
            "asiaticos de cabelo castanho",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'asiatica' AND cor_cabelo = 'castanho'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar asiaticos de cabelo grisalho",
            "pessoas asiaticas com cabelo grisalho",
            "asiaticos de cabelo grisalho",
            "idosos asiaticos",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'asiatica' AND cor_cabelo = 'grisalho'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pardos de cabelo castanho",
            "pessoas pardas com cabelo castanho",
            "pardos de cabelo castanho",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'parda' AND cor_cabelo = 'castanho'",
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pardos de cabelo preto",
            "pessoas pardas com cabelo preto",
            "pardos de cabelo preto",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'parda' AND cor_cabelo = 'preto'",
        "kind": "rows",
    },

    # ===================== Combinacoes: cor_cabelo + faixa_etaria =====================
    {
        "phrases": [
            "mostrar idosos de cabelo grisalho",
            "pessoas idosas com cabelo grisalho",
            "idosos com cabelo grisalho",
            "velhinhos de cabelo grisalho",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'grisalho' AND faixa_etaria = '60+'",
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas de cabelo loiro",
            "mostrar criancas loiras",
            "criancas com cabelo loiro",
            "bebes loiros",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'loiro' AND faixa_etaria IN ('0-5', '5-12')",
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas de cabelo preto",
            "mostrar criancas de cabelo preto",
            "criancas com cabelo preto",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'preto' AND faixa_etaria IN ('0-5', '5-12')",
        "kind": "rows",
    },
    {
        "phrases": [
            "jovens de cabelo castanho",
            "mostrar jovens com cabelo castanho",
            "adolescentes de cabelo castanho",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'castanho' AND faixa_etaria IN ('13-17', '18-25')",
        "kind": "rows",
    },
    {
        "phrases": [
            "adultos de cabelo castanho",
            "mostrar adultos com cabelo castanho",
            "pessoas de meia idade de cabelo castanho",
        ],
        "sql": "SELECT * FROM people_images WHERE cor_cabelo = 'castanho' AND faixa_etaria IN ('26-40', '41-60')",
        "kind": "rows",
    },

    # ===================== Combinacoes: etnia + faixa_etaria =====================
    {
        "phrases": [
            "criancas negras",
            "mostrar criancas negras",
            "criancas de etnia negra",
            "bebes negros",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'negra' AND faixa_etaria IN ('0-5', '5-12')",
        "kind": "rows",
    },
    {
        "phrases": [
            "adolescentes negros",
            "jovens negros",
            "mostrar jovens negros",
            "adolescentes de etnia negra",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'negra' AND faixa_etaria IN ('13-17', '18-25')",
        "kind": "rows",
    },
    {
        "phrases": [
            "idosos brancos",
            "mostrar idosos brancos",
            "pessoas brancas idosas",
            "idosos de etnia branca",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'branca' AND faixa_etaria = '60+'",
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas asiaticas",
            "mostrar criancas asiaticas",
            "criancas de etnia asiatica",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'asiatica' AND faixa_etaria IN ('0-5', '5-12')",
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas pardas",
            "mostrar criancas pardas",
            "criancas de etnia parda",
        ],
        "sql": "SELECT * FROM people_images WHERE etnia = 'parda' AND faixa_etaria IN ('0-5', '5-12')",
        "kind": "rows",
    },
]
