"""
Camada de NLP para busca semântica (PC7).

Pipeline aplicado tanto às frases canônicas (catálogo em queries.INTENTS)
quanto à entrada do usuário, na seguinte ordem:

  1. Normalização:
     - lowercase
     - remoção de acentos (NFKD + filtro de combining marks)
  2. Tokenização: regex `[a-z0-9]+` (descarta pontuação).
  3. Remoção de stopwords PT-BR (NLTK), comparadas SEM acento.
  4. Stemming PT-BR com RSLPStemmer (NLTK) — reduz "loiro/loiras",
     "pessoa/pessoas", "branco/brancas" a um radical comum.
  5. Vetorização Bag-of-Words com CountVectorizer (sklearn).
  6. Match: similaridade de cosseno entre o BOW da entrada e o BOW
     de cada frase canônica. Se o melhor score ficar abaixo de
     SIMILARITY_THRESHOLD a função devolve (None, score) — o app
     responde "não entendi" em vez de chutar uma SQL qualquer.

A vantagem desse pipeline é que variações naturais como
"mostrar pessoas com cabelo loiro", "pessoas loiras" e
"quem tem cabelo loiro" caem todas no mesmo bag-of-stems
("pesso loir"-ish) e batem na mesma intent.
"""

from __future__ import annotations

import re
import unicodedata

import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from queries import INTENTS

# Limiar mínimo de similaridade para aceitar uma intent. Abaixo disso,
# consideramos que a pergunta não corresponde a nenhuma intent conhecida.
SIMILARITY_THRESHOLD = 0.20


def _ensure_nltk_resources() -> None:
    """Baixa stopwords e o stemmer RSLP no primeiro uso (idempotente)."""
    for path, pkg in (("corpora/stopwords", "stopwords"), ("stemmers/rslp", "rslp")):
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)


_ensure_nltk_resources()

_STEMMER = RSLPStemmer()
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


# As stopwords do NLTK vêm com acento ("não", "são", "estão"). Como o
# pipeline tira o acento ANTES de filtrar, geramos uma versão também sem
# acento para o set de comparação.
_STOPWORDS_PT = {_strip_accents(w) for w in stopwords.words("portuguese")}


def preprocess(text: str) -> str:
    """Aplica normalização → tokenização → stopwords → stemming.

    Retorna a string final pronta para ser vetorizada (tokens separados
    por espaço). String vazia indica que sobrou nada após filtragem.
    """
    text = _strip_accents(text.lower())
    tokens = _TOKEN_RE.findall(text)
    tokens = [t for t in tokens if t not in _STOPWORDS_PT]
    tokens = [_STEMMER.stem(t) for t in tokens]
    return " ".join(tokens)


# Achata o catálogo INTENTS em dois vetores paralelos:
#   _PHRASES[i]            → frase canônica i, já pré-processada
#   _PHRASE_TO_INTENT[i]   → índice da intent à qual a frase i pertence
# Cada intent contribui várias frases para o BOW, todas apontando de
# volta para o mesmo dicionário em INTENTS.
_PHRASES: list[str] = []
_PHRASE_TO_INTENT: list[int] = []
for _idx, _intent in enumerate(INTENTS):
    for _phrase in _intent["phrases"]:
        _PHRASES.append(preprocess(_phrase))
        _PHRASE_TO_INTENT.append(_idx)

_VECTORIZER = CountVectorizer()
_BOW_MATRIX = _VECTORIZER.fit_transform(_PHRASES)


def find_best_intent(user_input: str) -> tuple[int | None, float]:
    """Retorna (índice_da_intent, score_cosseno) para a entrada do usuário.

    Se o input ficar vazio após o pré-processamento, ou se nenhum token
    do input estiver no vocabulário do BOW, ou se o melhor cosseno ficar
    abaixo de SIMILARITY_THRESHOLD, retorna (None, score) e cabe ao
    chamador tratar como "intenção não reconhecida".
    """
    processed = preprocess(user_input)
    if not processed:
        return None, 0.0

    user_vec = _VECTORIZER.transform([processed])
    if user_vec.nnz == 0:
        # Nenhum token do usuário aparece no vocabulário das frases
        # canônicas → cosseno seria 0 com qualquer linha.
        return None, 0.0

    sims = cosine_similarity(user_vec, _BOW_MATRIX).flatten()
    best_phrase_idx = int(sims.argmax())
    best_score = float(sims[best_phrase_idx])
    if best_score < SIMILARITY_THRESHOLD:
        return None, best_score
    return _PHRASE_TO_INTENT[best_phrase_idx], best_score
