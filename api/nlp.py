"""
Camada de NLP — busca semântica com correção ortográfica.

Pipeline para ENTRADA DO USUÁRIO:
  0. Correção ortográfica via pyspellchecker (vocabulário do domínio extraído de INTENTS)
  1. Normalização: lowercase + remoção de acentos (NFKD)
  2. Tokenização: regex [a-z0-9]+
  3. Remoção de stopwords PT-BR (NLTK)
  4. Stemming PT-BR com RSLPStemmer (NLTK)
  5. Vetorização Bag-of-Words (CountVectorizer, sklearn)
  6. Cosseno contra frases canônicas pré-processadas

Frases canônicas passam apenas pelas etapas 1–5 (sem correção ortográfica).
"""

from __future__ import annotations

import re
import unicodedata

import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spellchecker import SpellChecker

from queries import INTENTS

SIMILARITY_THRESHOLD = 0.20


def _ensure_nltk_resources() -> None:
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


# Stopwords PT-BR do NLTK (accent-stripped para bater com o pipeline).
_STOPWORDS_PT = {_strip_accents(w) for w in stopwords.words("portuguese")}

_DOMAIN_STOPWORDS = {
    "cadastrado", "cadastrada", "cadastrados", "cadastradas",
    "imagem", "imagens", "foto", "fotos",
}
_STOPWORDS_PT |= _DOMAIN_STOPWORDS


def _build_spell_checker() -> SpellChecker:
    """SpellChecker sem dicionário padrão, treinado no vocabulário das intenções.

    Usar language=None evita conflito entre dicionário PT acentuado e o pipeline
    que opera sem acentos. O vocabulário cobre todo termo das frases canônicas
    mais auxiliares comuns que podem aparecer em variações livres do usuário.
    """
    spell = SpellChecker(language=None)
    domain: set[str] = set()
    for intent in INTENTS:
        for phrase in intent["phrases"]:
            words = re.findall(r"[a-z]+", _strip_accents(phrase.lower()))
            domain.update(words)
    domain.update({
        "pessoas", "pessoa", "mostrar", "listar", "exibir", "mostre", "liste",
        "exiba", "quem", "quais", "quantas", "quantos", "qual", "numero",
        "total", "existem", "existe", "tem", "sao", "cadastradas", "cadastrados",
        "cadastrada", "cadastrado", "todas", "todos", "algumas", "alguns",
        "com", "sem", "por", "para", "que", "como", "imagem", "imagens",
    })
    spell.word_frequency.load_words(domain)
    return spell


_SPELL = _build_spell_checker()


def _correct_spelling(text: str) -> str:
    """
    correção de erros ja estando sem acento e com minusculas, só os tokens corretamente processados
    são avalidados numeros, simbolos e coisa do tipo passa sem modificação se o spell não pegar uma
    palavra valida ele mantem o token original
    """
    tokens = text.split()
    alpha = [t for t in tokens if t.isalpha()]
    unknown = _SPELL.unknown(alpha)
    result = []
    for token in tokens:
        if token in unknown:
            fixed = _SPELL.correction(token)
            result.append(fixed if fixed else token)
        else:
            result.append(token)
    return " ".join(result)


def preprocess(text: str) -> str:
    """Pipeline para frases canônicas: normalização → tokenização → stopwords → stemming."""
    text = _strip_accents(text.lower())
    tokens = _TOKEN_RE.findall(text)
    tokens = [t for t in tokens if t not in _STOPWORDS_PT]
    tokens = [_STEMMER.stem(t) for t in tokens]
    return " ".join(tokens)


def preprocess_user_input(text: str) -> str:
    """
    agora a ordem fica: normalização → correção ortográfica → tokenização → stopwords → stemming.
    os intervalos númericos ficam em app.py
    """
    text = _strip_accents(text.lower())
    text = _correct_spelling(text)
    tokens = _TOKEN_RE.findall(text)
    tokens = [t for t in tokens if t not in _STOPWORDS_PT]
    tokens = [_STEMMER.stem(t) for t in tokens]
    return " ".join(tokens)


# Achata o catálogo INTENTS: cada frase canônica pré-processada mapeada ao índice da intent.
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

    Devolve (None, score) se o input ficar vazio, sem tokens no vocabulário,
    ou se o cosseno ficar abaixo de SIMILARITY_THRESHOLD.
    """
    processed = preprocess_user_input(user_input)
    if not processed:
        return None, 0.0

    user_vec = _VECTORIZER.transform([processed])
    if user_vec.nnz == 0:
        return None, 0.0

    sims = cosine_similarity(user_vec, _BOW_MATRIX).flatten()
    best_phrase_idx = int(sims.argmax())
    best_score = float(sims[best_phrase_idx])
    if best_score < SIMILARITY_THRESHOLD:
        return None, best_score
    return _PHRASE_TO_INTENT[best_phrase_idx], best_score
