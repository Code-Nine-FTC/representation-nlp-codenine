# Pipeline de Busca Semântica (PC.7)

## Visão geral da arquitetura

Cada responsabilidade vive em uma classe própria (`api/semantic.py`),
orquestradas pela classe `Pipeline`.

| Classe | Responsabilidade |
| --- | --- |
| `Normalizador` | Minúsculas, remoção de acentos, tokenização e geração de trechos (n-gramas). |
| `Corretor` | Correção ortográfica (`pyspellchecker`) com vocabulário do domínio. |
| `TipoConsulta` | Decide entre contagem (`count`) e listagem (`rows`). |
| `IdadeNumerica` | Extrai intervalos de idade explícitos por expressões regulares. |
| `MotorSemantico` | Classe base: indexa as sementes e classifica os trechos por cosseno. |
| `MotorTransformer` | Representação com `sentence-transformers`. |
| `MotorWord2Vec` | Representação com `gensim.Word2Vec` treinado no domínio. |
| `ConstrutorSql` | Monta a SQL final a partir das condições coletadas. |
| `Pipeline` | Encadeia as etapas, escolhe o motor e devolve um `Resultado`. |

O vocabulário de domínio (categorias, condições SQL e sementes) fica isolado em
`api/vocabulary.py` (`Categoria`, `GrupoSemantico`).

```
texto do usuário
      │
      ▼
┌──────────────┐   ┌──────────┐   ┌──────────────┐   ┌────────────────┐
│ Normalizador │ → │ Corretor │ → │ TipoConsulta │ → │ IdadeNumerica  │
└──────────────┘   └──────────┘   └──────────────┘   └────────────────┘
      │                                                       │
      ▼                                                       │
┌──────────────────────────────────────────┐                │
│ MotorSemantico (Word2Vec | Transformer)   │                │
└──────────────────────────────────────────┘                │
      │                                                       │
      └───────────────────────┬───────────────────────────────┘
                              ▼
                      ┌──────────────┐
                      │ ConstrutorSql│ → SQL → PostgreSQL → JSON → Interface
                      └──────────────┘
```

---

## Etapa 1 — Normalização

`Normalizador.normalizar` coloca o texto em minúsculas e remove acentos via
`unicodedata` (NFKD), alinhando a entrada (frequentemente sem acento) ao
vocabulário.

```
"Quantos IDOSOS Asiáticos existem?"  →  "quantos idosos asiaticos existem"
```

## Etapa 2 — Correção ortográfica

`Corretor.corrigir` usa o `pyspellchecker` com um dicionário **montado a partir
do domínio** (todas as palavras das sementes + termos auxiliares de etnia, cor,
faixa etária e formulação). Tokens desconhecidos são trocados pela palavra mais
próxima; números e símbolos passam intactos.

```
"pesoas negras jovns"  →  "pessoas negras jovens"
"asiatcos"             →  "asiaticos"
```

## Etapa 3 — Tipo de consulta

`TipoConsulta.detectar` verifica se há termos de contagem (`quantos`, `total`,
`numero`, ...). Se sim, o tipo é `count`; caso contrário, `rows`.

## Etapa 4 — Idade numérica

`IdadeNumerica.condicao` captura idades explícitas via regex, com precedência:

| Padrão | Exemplo | Condição |
| --- | --- | --- |
| intervalo | `de 18 a 25 anos` | `idade BETWEEN 18 AND 25` |
| acima | `mais de 60 anos` | `idade > 60` |
| abaixo | `menos de 12 anos` | `idade < 12` |
| exata | `30 anos` | `idade = 30` |

A idade numérica tem prioridade sobre a faixa etária semântica.

## Etapa 5 — Geração de trechos

`Normalizador.trechos` descarta termos genéricos (`pessoas`, `mostrar`, `de`,
...) e dígitos, e gera **unigramas + bigramas**. Os bigramas preservam contexto
curto (`cabelo preto` vs. pessoa `preta`). Sem trechos relevantes, nenhum filtro
é aplicado e a consulta retorna todos os registros.

```
"mostrar pessoas com cabelo loiro"  →  ["cabelo", "loiro", "cabelo loiro"]
"quantas pessoas existem"           →  []
```

## Etapa 6 — Representação e correspondência

Cada motor herda de `MotorSemantico`. Na inicialização, as **sementes** de cada
categoria (frases-âncora como `pessoa negra`, `cabelo grisalho`, `vovô`) são
vetorizadas e guardadas. Em tempo de consulta, os trechos viram vetores e a
similaridade de cosseno é calculada; para cada grupo (`etnia`, `cor_cabelo`,
`faixa_etaria`) toma-se o maior score:

```
score(grupo) = max sobre (trecho × semente) de cos(trecho, semente)
```

### Motor Transformer (`sentence-transformers`)

Modelo `paraphrase-multilingual-mpnet-base-v2` rodando em CPU. Gera embeddings
contextuais das frases inteiras; **generaliza** para sinônimos e variações que
não estão nas sementes (ex.: `cabelo cinza` → grisalho), ao custo de mais ruído
em palavras isoladas.

### Motor Word2Vec (`gensim`)

Treinado na inicialização sobre um corpus do próprio domínio (sementes
*stemizadas* com `RSLPStemmer`). O vetor de um trecho é a **média** dos vetores
das suas palavras. É **preciso** no vocabulário conhecido e separa bem as
categorias, mas **não generaliza** para palavras que não viu no treino.

> Antes da representação, o Word2Vec aplica remoção de stopwords (NLTK) e
> *stemming*; o Transformer opera sobre o texto normalizado, deixando a
> morfologia para o próprio modelo.

## Etapa 7 — Limiar por grupo

Cada motor tem seus próprios limiares por grupo, pois as escalas de cosseno
diferem:

| Grupo | Transformer | Word2Vec |
| --- | --- | --- |
| `etnia` | 0.74 | 0.70 |
| `cor_cabelo` | 0.88 | 0.90 |
| `faixa_etaria` | 0.88 | 0.70 |

A categoria de maior score em um grupo só vira filtro se ultrapassar o limiar.

## Etapa 8 — Montagem da SQL

As categorias selecionadas contribuem com fragmentos pré-definidos e seguros
(ex.: `etnia = 'negra'`); a idade numérica acrescenta sua condição.
`ConstrutorSql.construir` produz:

- `count` → `SELECT COUNT(*) AS total FROM people_images WHERE ...`
- `rows`  → `SELECT id, nome, etnia, cor_cabelo, idade, label_etaria, caminho_imagem FROM people_images WHERE ...`

Os fragmentos são constantes do vocabulário, nunca texto do usuário — não há
injeção possível.

## Etapa 9 — Execução e resposta

`app.py` executa a SQL no PostgreSQL e devolve um JSON com `motor`, `sql`,
`kind`, `filtros`, `passos` (rastro de cada etapa) e `resultado`. Para `count`,
também retorna as fotos correspondentes. A interface (`static/chat.js`) renderiza
o motor usado, os filtros detectados, a SQL e os cartões das pessoas.

---

## Exemplo completo

Pergunta: **"pesoas negras jovns"** (com erros de digitação), motor Word2Vec

| Etapa | Saída |
| --- | --- |
| Normalização | `pesoas negras jovns` |
| Correção ortográfica | `pessoas negras jovens` |
| Tipo | `rows` |
| Idade numérica | `None` |
| Trechos | `negras`, `jovens`, `negras jovens` |
| Correspondência | `etnia=negra (0.99)`, `faixa_etaria=jovem (1.0)` |
| SQL | `... WHERE etnia = 'negra' AND idade BETWEEN 18 AND 25` |
| Resposta | 2 pessoas |

---

## Word2Vec vs. Transformer (resumo comparativo)

| | Word2Vec | Transformer |
| --- | --- | --- |
| Representação | média de vetores de palavras | embedding contextual da frase |
| Generalização a sinônimos novos | baixa (só o que viu no treino) | alta |
| Precisão no vocabulário conhecido | alta | alta, com algum ruído |
| Pré-processamento | normalização → correção → stopwords → stemming | normalização → correção |
| Custo | treino leve na inicialização | modelo baixado uma vez (~1 GB em cache) |

---

## Como executar

```bash
docker compose up -d                 # sobe o PostgreSQL com init.sql
pip install -r requirements.txt      # Flask + sentence-transformers + gensim + nltk
python api/app.py                     # 1ª execução baixa o modelo Transformer
```

O modelo `paraphrase-multilingual-mpnet-base-v2` é baixado uma vez pelo
`sentence-transformers` e fica em cache; o Word2Vec é treinado a cada
inicialização (rápido). Os recursos do NLTK (`stopwords`, `rslp`) são baixados
automaticamente na primeira execução.
