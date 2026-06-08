"""
Intenções para busca semântica por linguagem natural sobre people_images.

Cada intent contém:
  phrases  – variações sem acento que o usuário pode digitar
  sql      – SQL a executar no Postgres
  kind     – 'count' (escalar) ou 'rows' (lista de pessoas com foto)

Todas as queries 'rows' usam _S() para selecionar explicitamente
caminho_imagem, label_etaria e idade.
"""


def _S(where: str = "") -> str:
    base = (
        "SELECT id, nome, etnia, cor_cabelo, idade, "
        "label_etaria, caminho_imagem FROM people_images"
    )
    return base if not where else f"{base} WHERE {where}"


INTENTS = [
    # ===================== Contagens gerais =====================
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
            "quantos cadastros existem",
            "qual o tamanho do banco",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images",
        "kind": "count",
    },

    # ===================== Contagens por etnia =====================
    {
        "phrases": [
            "quantas pessoas brancas existem",
            "total de pessoas brancas",
            "numero de pessoas de etnia branca",
            "quantos brancos estao cadastrados",
            "quantas pessoas da etnia branca",
            "total de brancos",
            "quantos brancos existem",
            "quantidade de pessoas brancas",
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
            "quantidade de pessoas negras",
            "quantas pessoas pretas existem",
            "total de pessoas pretas",
            "quantos pretos existem",
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
            "quantidade de pessoas pardas",
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
            "quantidade de pessoas asiaticas",
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
            "quantidade de pessoas indigenas",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE etnia = 'indigena'",
        "kind": "count",
    },

    # ===================== Contagens por faixa etária =====================
    {
        "phrases": [
            "quantos bebes existem",
            "total de bebes cadastrados",
            "quantas criancas de 0 a 5 anos",
            "quantas criancas pequenas existem",
            "numero de bebes no banco",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE idade <= 5",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas criancas existem",
            "total de criancas",
            "quantas pessoas tem menos de 12 anos",
            "numero de criancas cadastradas",
            "quantas criancas em idade escolar",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE idade <= 12",
        "kind": "count",
    },
    {
        "phrases": [
            "quantos adolescentes existem",
            "total de adolescentes cadastrados",
            "quantas pessoas de 13 a 17 anos",
            "numero de adolescentes",
            "quantos jovens de 13 a 17 anos",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE idade BETWEEN 13 AND 17",
        "kind": "count",
    },
    {
        "phrases": [
            "quantos jovens existem",
            "total de jovens cadastrados",
            "quantas pessoas de 18 a 25 anos",
            "quantos jovens adultos existem",
            "numero de jovens no banco",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE idade BETWEEN 18 AND 25",
        "kind": "count",
    },
    {
        "phrases": [
            "quantos adultos existem",
            "total de adultos cadastrados",
            "quantas pessoas de 26 a 40 anos",
            "numero de adultos no banco",
            "quantas pessoas adultas",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE idade BETWEEN 26 AND 40",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas de meia idade existem",
            "total de pessoas de 41 a 60 anos",
            "quantas pessoas de 41 a 60",
            "numero de pessoas de meia idade",
            "quantos de meia idade estao cadastrados",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE idade BETWEEN 41 AND 60",
        "kind": "count",
    },
    {
        "phrases": [
            "quantos idosos existem",
            "quantas pessoas tem mais de 60 anos",
            "total de idosos",
            "numero de idosos cadastrados",
            "quantas pessoas da terceira idade",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE idade > 60",
        "kind": "count",
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

    # ===================== Contagens por cor de cabelo =====================
    {
        "phrases": [
            "quantas pessoas tem cabelo loiro",
            "total de pessoas loiras",
            "numero de pessoas de cabelo loiro",
            "quantos loiros existem",
            "quantidade de pessoas com cabelo loiro",
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
            "quantidade de pessoas com cabelo preto",
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
            "quantidade de pessoas com cabelo castanho",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE cor_cabelo = 'castanho'",
        "kind": "count",
    },
    {
        "phrases": [
            "quantas pessoas ruivas existem",
            "total de pessoas ruivas",
            "numero de pessoas de cabelo ruivo",
            "quantos ruivos existem",
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
            "quantidade de pessoas com cabelo grisalho",
        ],
        "sql": "SELECT COUNT(*) AS total FROM people_images WHERE cor_cabelo = 'grisalho'",
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
            "mostrar todas as fotos",
            "ver todos os cadastros",
        ],
        "sql": _S(),
        "kind": "rows",
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
            "ver pessoas loiras",
        ],
        "sql": _S("cor_cabelo = 'loiro'"),
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
            "ver pessoas de cabelo preto",
        ],
        "sql": _S("cor_cabelo = 'preto'"),
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
        "sql": _S("cor_cabelo = 'castanho'"),
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
            "pessoas ruivas",
        ],
        "sql": _S("cor_cabelo = 'ruivo'"),
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
        "sql": _S("cor_cabelo = 'grisalho'"),
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
            "ver pessoas brancas",
        ],
        "sql": _S("etnia = 'branca'"),
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
            "ver pessoas negras",
            "mostrar pessoas pretas",
            "pessoas pretas",
            "listar pessoas pretas",
            "pretos e pretas",
        ],
        "sql": _S("etnia = 'negra'"),
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
            "ver pessoas pardas",
        ],
        "sql": _S("etnia = 'parda'"),
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
            "ver pessoas asiaticas",
        ],
        "sql": _S("etnia = 'asiatica'"),
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
            "ver pessoas indigenas",
        ],
        "sql": _S("etnia = 'indigena'"),
        "kind": "rows",
    },

    # ===================== Seleção por faixa etária =====================
    {
        "phrases": [
            "mostrar bebes",
            "pessoas de 0 a 5 anos",
            "criancas de 0 a 5 anos",
            "lista de bebes",
            "mostre os bebes",
            "criancas pequenas",
            "bebes de 0 a 5 anos",
            "criancas de 0 a 5",
            "ver bebes",
        ],
        "sql": _S("idade <= 5"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar criancas",
            "pessoas de 5 a 12 anos",
            "criancas de 5 a 12 anos",
            "criancas de 5 a 12",
            "mostre as criancas",
            "criancas em idade escolar",
            "menores de 12 anos",
            "ver criancas",
            "listar criancas",
        ],
        "sql": _S("idade BETWEEN 6 AND 12"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar adolescentes",
            "pessoas de 13 a 17 anos",
            "listar adolescentes",
            "mostre os adolescentes",
            "jovens de 13 a 17 anos",
            "adolescentes de 13 a 17",
            "ver adolescentes",
            "jovens adolescentes",
        ],
        "sql": _S("idade BETWEEN 13 AND 17"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar jovens",
            "pessoas de 18 a 25 anos",
            "listar jovens",
            "mostre os jovens",
            "jovens de 18 a 25 anos",
            "pessoas jovens",
            "maiores de idade",
            "jovens adultos",
            "ver jovens",
        ],
        "sql": _S("idade BETWEEN 18 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar adultos",
            "pessoas de 26 a 40 anos",
            "listar adultos",
            "mostre os adultos",
            "adultos de 26 a 40 anos",
            "pessoas de 26 a 40",
            "ver adultos",
        ],
        "sql": _S("idade BETWEEN 26 AND 40"),
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
            "ver pessoas de meia idade",
        ],
        "sql": _S("idade BETWEEN 41 AND 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar idosos",
            "pessoas com mais de 60 anos",
            "listar idosos",
            "mostre os idosos",
            "pessoas idosas",
            "terceira idade",
            "melhor idade",
            "acima de 60 anos",
            "ver idosos",
            "pessoas da terceira idade",
        ],
        "sql": _S("idade > 60"),
        "kind": "rows",
    },

    # ===================== Combinações: etnia + cor_cabelo =====================
    {
        "phrases": [
            "mostrar brancos de cabelo loiro",
            "pessoas brancas com cabelo loiro",
            "brancos loiros",
            "exiba pessoas brancas de cabelo loiro",
            "liste brancos com cabelo loiro",
        ],
        "sql": _S("etnia = 'branca' AND cor_cabelo = 'loiro'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar brancos de cabelo preto",
            "pessoas brancas com cabelo preto",
            "brancos de cabelo preto",
        ],
        "sql": _S("etnia = 'branca' AND cor_cabelo = 'preto'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar brancos de cabelo castanho",
            "pessoas brancas com cabelo castanho",
            "brancos de cabelo castanho",
        ],
        "sql": _S("etnia = 'branca' AND cor_cabelo = 'castanho'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar brancos de cabelo grisalho",
            "pessoas brancas com cabelo grisalho",
            "brancos de cabelo grisalho",
        ],
        "sql": _S("etnia = 'branca' AND cor_cabelo = 'grisalho'"),
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
        "sql": _S("etnia = 'negra' AND cor_cabelo = 'preto'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar negros de cabelo castanho",
            "pessoas negras com cabelo castanho",
            "negros de cabelo castanho",
        ],
        "sql": _S("etnia = 'negra' AND cor_cabelo = 'castanho'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar negros de cabelo loiro",
            "pessoas negras com cabelo loiro",
            "negros de cabelo loiro",
        ],
        "sql": _S("etnia = 'negra' AND cor_cabelo = 'loiro'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar asiaticos de cabelo preto",
            "pessoas asiaticas com cabelo preto",
            "asiaticos de cabelo preto",
        ],
        "sql": _S("etnia = 'asiatica' AND cor_cabelo = 'preto'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar asiaticos de cabelo castanho",
            "pessoas asiaticas com cabelo castanho",
            "asiaticos de cabelo castanho",
        ],
        "sql": _S("etnia = 'asiatica' AND cor_cabelo = 'castanho'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar asiaticos de cabelo grisalho",
            "pessoas asiaticas com cabelo grisalho",
            "asiaticos de cabelo grisalho",
        ],
        "sql": _S("etnia = 'asiatica' AND cor_cabelo = 'grisalho'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pardos de cabelo castanho",
            "pessoas pardas com cabelo castanho",
            "pardos de cabelo castanho",
        ],
        "sql": _S("etnia = 'parda' AND cor_cabelo = 'castanho'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar pardos de cabelo preto",
            "pessoas pardas com cabelo preto",
            "pardos de cabelo preto",
        ],
        "sql": _S("etnia = 'parda' AND cor_cabelo = 'preto'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar indigenas de cabelo preto",
            "pessoas indigenas com cabelo preto",
            "indigenas de cabelo preto",
        ],
        "sql": _S("etnia = 'indigena' AND cor_cabelo = 'preto'"),
        "kind": "rows",
    },
    {
        "phrases": [
            "mostrar indigenas de cabelo castanho",
            "pessoas indigenas com cabelo castanho",
            "indigenas de cabelo castanho",
        ],
        "sql": _S("etnia = 'indigena' AND cor_cabelo = 'castanho'"),
        "kind": "rows",
    },

    # ===================== Combinações: cor_cabelo + faixa etária =====================
    {
        "phrases": [
            "mostrar idosos de cabelo grisalho",
            "pessoas idosas com cabelo grisalho",
            "idosos com cabelo grisalho",
            "velhinhos de cabelo grisalho",
        ],
        "sql": _S("cor_cabelo = 'grisalho' AND idade > 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas de cabelo loiro",
            "mostrar criancas loiras",
            "criancas com cabelo loiro",
            "bebes loiros",
        ],
        "sql": _S("cor_cabelo = 'loiro' AND idade <= 12"),
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas de cabelo preto",
            "mostrar criancas de cabelo preto",
            "criancas com cabelo preto",
            "bebes de cabelo preto",
        ],
        "sql": _S("cor_cabelo = 'preto' AND idade <= 12"),
        "kind": "rows",
    },
    {
        "phrases": [
            "jovens de cabelo castanho",
            "mostrar jovens com cabelo castanho",
            "adolescentes de cabelo castanho",
        ],
        "sql": _S("cor_cabelo = 'castanho' AND idade BETWEEN 13 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "adultos de cabelo castanho",
            "mostrar adultos com cabelo castanho",
            "pessoas de meia idade de cabelo castanho",
        ],
        "sql": _S("cor_cabelo = 'castanho' AND idade BETWEEN 26 AND 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "jovens de cabelo loiro",
            "mostrar jovens loiros",
            "adolescentes de cabelo loiro",
            "jovens adultos de cabelo loiro",
        ],
        "sql": _S("cor_cabelo = 'loiro' AND idade BETWEEN 13 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "adultos de cabelo grisalho",
            "pessoas de meia idade de cabelo grisalho",
            "meia idade com cabelo grisalho",
        ],
        "sql": _S("cor_cabelo = 'grisalho' AND idade BETWEEN 26 AND 60"),
        "kind": "rows",
    },

    # ===================== Combinações: etnia + faixa etária =====================
    {
        "phrases": [
            "criancas negras",
            "mostrar criancas negras",
            "criancas de etnia negra",
            "bebes negros",
            "criancas e bebes negros",
            "criancas pretas",
            "bebes pretos",
        ],
        "sql": _S("etnia = 'negra' AND idade <= 12"),
        "kind": "rows",
    },
    {
        "phrases": [
            "adolescentes negros",
            "jovens negros",
            "mostrar jovens negros",
            "adolescentes de etnia negra",
            "negros adolescentes",
            "adolescentes pretos",
            "jovens pretos",
            "pessoas pretas jovens",
        ],
        "sql": _S("etnia = 'negra' AND idade BETWEEN 13 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "adultos negros",
            "pessoas negras adultas",
            "negros de 26 a 40 anos",
            "mostrar adultos negros",
            "adultos pretos",
            "pessoas pretas adultas",
            "pretos de 26 a 40 anos",
            "pessoas pretas adulto",
        ],
        "sql": _S("etnia = 'negra' AND idade BETWEEN 26 AND 40"),
        "kind": "rows",
    },
    {
        "phrases": [
            "negros de meia idade",
            "pessoas negras de meia idade",
            "negros de 41 a 60 anos",
            "mostrar negros de meia idade",
            "pretos de meia idade",
            "pessoas pretas de meia idade",
            "pretos de 41 a 60 anos",
            "pessoas pretas meia idade",
        ],
        "sql": _S("etnia = 'negra' AND idade BETWEEN 41 AND 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "idosos negros",
            "pessoas negras idosas",
            "negros idosos",
            "mostrar idosos negros",
            "idosos pretos",
            "pessoas pretas idosas",
            "pretos idosos",
        ],
        "sql": _S("etnia = 'negra' AND idade > 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "idosos brancos",
            "mostrar idosos brancos",
            "pessoas brancas idosas",
            "idosos de etnia branca",
        ],
        "sql": _S("etnia = 'branca' AND idade > 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas brancas",
            "mostrar criancas brancas",
            "criancas de etnia branca",
            "bebes brancos",
        ],
        "sql": _S("etnia = 'branca' AND idade <= 12"),
        "kind": "rows",
    },
    {
        "phrases": [
            "jovens brancos",
            "adolescentes brancos",
            "pessoas brancas jovens",
            "mostrar jovens brancos",
        ],
        "sql": _S("etnia = 'branca' AND idade BETWEEN 13 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas asiaticas",
            "mostrar criancas asiaticas",
            "criancas de etnia asiatica",
            "bebes asiaticos",
        ],
        "sql": _S("etnia = 'asiatica' AND idade <= 12"),
        "kind": "rows",
    },
    {
        "phrases": [
            "jovens asiaticos",
            "adolescentes asiaticos",
            "pessoas asiaticas jovens",
            "mostrar jovens asiaticos",
        ],
        "sql": _S("etnia = 'asiatica' AND idade BETWEEN 13 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "idosos asiaticos",
            "pessoas asiaticas idosas",
            "asiaticos idosos",
            "mostrar idosos asiaticos",
        ],
        "sql": _S("etnia = 'asiatica' AND idade > 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas pardas",
            "mostrar criancas pardas",
            "criancas de etnia parda",
            "bebes pardos",
        ],
        "sql": _S("etnia = 'parda' AND idade <= 12"),
        "kind": "rows",
    },
    {
        "phrases": [
            "adultos pardos",
            "pessoas pardas adultas",
            "pardos adultos",
            "mostrar adultos pardos",
        ],
        "sql": _S("etnia = 'parda' AND idade BETWEEN 26 AND 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "adultos indigenas",
            "pessoas indigenas adultas",
            "indigenas adultos",
            "mostrar adultos indigenas",
        ],
        "sql": _S("etnia = 'indigena' AND idade BETWEEN 26 AND 60"),
        "kind": "rows",
    },

    # ===================== Combinações triplas: etnia + cor_cabelo + faixa etária =====================
    {
        "phrases": [
            "idosos brancos de cabelo grisalho",
            "pessoas brancas idosas com cabelo grisalho",
            "brancos idosos de cabelo grisalho",
        ],
        "sql": _S("etnia = 'branca' AND cor_cabelo = 'grisalho' AND idade > 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "jovens brancos de cabelo loiro",
            "adolescentes brancos loiros",
            "pessoas brancas jovens de cabelo loiro",
        ],
        "sql": _S("etnia = 'branca' AND cor_cabelo = 'loiro' AND idade BETWEEN 13 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "jovens negros de cabelo preto",
            "adolescentes negros de cabelo preto",
            "negros jovens de cabelo preto",
        ],
        "sql": _S("etnia = 'negra' AND cor_cabelo = 'preto' AND idade BETWEEN 13 AND 25"),
        "kind": "rows",
    },
    {
        "phrases": [
            "adultos pardos de cabelo castanho",
            "pessoas pardas adultas com cabelo castanho",
            "pardos adultos de cabelo castanho",
        ],
        "sql": _S("etnia = 'parda' AND cor_cabelo = 'castanho' AND idade BETWEEN 26 AND 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "idosos asiaticos de cabelo grisalho",
            "pessoas asiaticas idosas de cabelo grisalho",
            "asiaticos idosos de cabelo grisalho",
        ],
        "sql": _S("etnia = 'asiatica' AND cor_cabelo = 'grisalho' AND idade > 60"),
        "kind": "rows",
    },
    {
        "phrases": [
            "criancas brancas de cabelo loiro",
            "bebes brancos de cabelo loiro",
            "criancas brancas loiras",
        ],
        "sql": _S("etnia = 'branca' AND cor_cabelo = 'loiro' AND idade <= 12"),
        "kind": "rows",
    },
]
