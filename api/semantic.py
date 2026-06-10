from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

import numpy as np
import nltk
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from sentence_transformers import SentenceTransformer
from spellchecker import SpellChecker

from vocabulary import GRUPOS, Categoria, GrupoSemantico

MODELO_TRANSFORMER = "paraphrase-multilingual-mpnet-base-v2"

LIMIARES_TRANSFORMER = {"etnia": 0.74, "cor_cabelo": 0.88, "faixa_etaria": 0.88}
LIMIARES_WORD2VEC = {"etnia": 0.70, "cor_cabelo": 0.90, "faixa_etaria": 0.70}

_PESO_TRANSFORMER = 0.6

TERMOS_CONTAGEM = frozenset({
    "quantos", "quantas", "quanto", "quantidade", "total",
    "numero", "qnts", "qntas", "qtd",
})

TERMOS_GENERICOS = frozenset({
    "mostrar", "mostre", "mostra", "listar", "liste", "lista", "exibir",
    "exiba", "exibe", "ver", "quero", "gostaria", "me", "quais", "qual",
    "quantos", "quantas", "quanto", "quantidade", "total", "numero", "qnts",
    "qntas", "qtd", "existe", "existem", "ha", "tem", "temos", "sao", "e",
    "pessoa", "pessoas", "gente", "individuo", "individuos", "registro",
    "registros", "cadastrado", "cadastrados", "cadastrada", "cadastradas",
    "banco", "catalogo", "imagem", "imagens", "foto", "fotos", "todas",
    "todos", "toda", "todo", "os", "as", "o", "a", "de", "do", "da", "dos",
    "das", "com", "sem", "ou", "que", "um", "uma", "no", "na", "por", "para",
    "sobre", "cada", "aqui", "essa", "esse", "quem", "anos", "ano",
    "mais", "menos", "maior", "menor", "acima", "abaixo", "partir",
    "entre", "ate",
})

VOCABULARIO_AUXILIAR = frozenset({
    "branco", "brancos", "branca", "brancas", "negro", "negros", "negra",
    "negras", "preto", "pretos", "preta", "pretas", "pardo", "pardos",
    "parda", "pardas", "moreno", "morenos", "morena", "morenas", "mulato",
    "asiatico", "asiaticos", "asiatica", "asiaticas", "oriental", "orientais",
    "indigena", "indigenas", "indio", "indios", "nativo", "nativos",
    "caucasiano", "afrodescendente", "loiro", "loiros", "loira", "loiras",
    "louro", "louros", "castanho", "castanhos", "castanha", "castanhas",
    "ruivo", "ruivos", "ruiva", "ruivas", "grisalho", "grisalhos", "cinza",
    "prateado", "prateados", "dourado", "dourados", "cabelo", "cabelos",
    "bebe", "bebes", "nenem", "nenens", "crianca", "criancas", "menino",
    "meninos", "menina", "meninas", "adolescente", "adolescentes", "jovem",
    "jovens", "rapaz", "moca", "mocas", "adulto", "adultos", "idoso",
    "idosos", "idosa", "idosas", "velho", "velhos", "velha", "velhas",
    "vovo", "vovos", "anciao", "etnia", "idade",
})


def _ensure_nltk() -> None:
    for caminho, pacote in (("corpora/stopwords", "stopwords"), ("stemmers/rslp", "rslp")):
        try:
            nltk.data.find(caminho)
        except LookupError:
            nltk.download(pacote, quiet=True)


_ensure_nltk()


class Normalizador:
    _palavra = re.compile(r"\w+", re.UNICODE)

    def sem_acento(self, texto: str) -> str:
        decomposto = unicodedata.normalize("NFKD", texto)
        return "".join(c for c in decomposto if not unicodedata.combining(c))

    def normalizar(self, texto: str) -> str:
        return self.sem_acento(texto.lower())

    def tokens(self, texto: str) -> list[str]:
        return self._palavra.findall(self.normalizar(texto))

    def trechos(self, texto: str) -> list[str]:
        tokens = [
            t for t in self.tokens(texto)
            if t not in TERMOS_GENERICOS and not t.isdigit()
        ]
        if not tokens:
            return []
        bigramas = [f"{a} {b}" for a, b in zip(tokens, tokens[1:])]
        return tokens + bigramas


class Corretor:
    def __init__(self, normalizador: Normalizador, grupos: tuple[GrupoSemantico, ...] = GRUPOS):
        self._normalizador = normalizador
        self._spell = SpellChecker(language="pt")
        self._spell.word_frequency.load_words(self._dominio(grupos))

    def _dominio(self, grupos: tuple[GrupoSemantico, ...]) -> set[str]:
        dominio: set[str] = set()
        for grupo in grupos:
            for categoria in grupo.categorias:
                for semente in categoria.sementes:
                    dominio.update(self._normalizador.tokens(semente))
        dominio |= TERMOS_GENERICOS | TERMOS_CONTAGEM | VOCABULARIO_AUXILIAR
        return dominio

    def corrigir(self, texto: str) -> str:
        tokens = texto.split()
        alfabeticos = [t for t in tokens if t.isalpha()]
        desconhecidos = self._spell.unknown(alfabeticos)
        corrigidos = []
        for token in tokens:
            if token in desconhecidos:
                sugestao = self._spell.correction(token)
                corrigidos.append(sugestao if sugestao else token)
            else:
                corrigidos.append(token)
        return " ".join(corrigidos)


class TipoConsulta:
    def __init__(self, termos: frozenset[str] = TERMOS_CONTAGEM):
        self._termos = termos

    def detectar(self, tokens: list[str]) -> str:
        return "count" if any(t in self._termos for t in tokens) else "rows"


class IdadeNumerica:
    _intervalo = re.compile(r"\b(\d{1,3})\s+[ae]\s+(\d{1,3})")
    _acima = re.compile(r"(?:acima|mais|maior|partir)\s+de\s+(\d{1,3})")
    _abaixo = re.compile(r"(?:abaixo|menos|menor)\s+de\s+(\d{1,3})")
    _exato = re.compile(r"\b(\d{1,3})\s+anos?\b")

    def condicao(self, texto: str) -> str | None:
        intervalo = self._intervalo.search(texto)
        if intervalo:
            menor, maior = sorted((int(intervalo.group(1)), int(intervalo.group(2))))
            return f"idade BETWEEN {menor} AND {maior}"
        acima = self._acima.search(texto)
        if acima:
            return f"idade > {int(acima.group(1))}"
        abaixo = self._abaixo.search(texto)
        if abaixo:
            return f"idade < {int(abaixo.group(1))}"
        exato = self._exato.search(texto)
        if exato:
            return f"idade = {int(exato.group(1))}"
        return None


class MotorSemantico:
    nome = "base"

    def __init__(self, limiares: dict[str, float], grupos: tuple[GrupoSemantico, ...] = GRUPOS):
        self._limiares = limiares
        self._grupos = grupos
        self._indice = {grupo.nome: self._indexar(grupo) for grupo in grupos}

    def _indexar(self, grupo: GrupoSemantico):
        referencias: list[Categoria] = []
        sementes: list[str] = []
        for categoria in grupo.categorias:
            for semente in categoria.sementes:
                referencias.append(categoria)
                sementes.append(semente)
        return referencias, self._vetorizar(sementes)

    def _vetorizar(self, textos: list[str]) -> np.ndarray:
        raise NotImplementedError

    def classificar(self, trechos: list[str]) -> dict[str, tuple[Categoria, float]]:
        if not trechos:
            return {}
        consulta = self._vetorizar(trechos)
        selecionados: dict[str, tuple[Categoria, float]] = {}
        for grupo in self._grupos:
            referencias, matriz = self._indice[grupo.nome]
            similaridades = consulta @ matriz.T
            melhor_por_semente = similaridades.max(axis=0)
            indice = int(melhor_por_semente.argmax())
            score = float(melhor_por_semente[indice])
            if score >= self._limiares[grupo.nome]:
                selecionados[grupo.nome] = (referencias[indice], score)
        return selecionados


class MotorTransformer(MotorSemantico):
    nome = "transformer"

    def __init__(
        self,
        normalizador: Normalizador,
        modelo: str = MODELO_TRANSFORMER,
        limiares: dict[str, float] = LIMIARES_TRANSFORMER,
        grupos: tuple[GrupoSemantico, ...] = GRUPOS,
    ):
        self._normalizador = normalizador
        self._codificador = SentenceTransformer(modelo)
        super().__init__(limiares, grupos)

    def _vetorizar(self, textos: list[str]) -> np.ndarray:
        normalizados = [self._normalizador.normalizar(t) for t in textos]
        return self._codificador.encode(
            normalizados, normalize_embeddings=True, convert_to_numpy=True
        )


class MotorWord2Vec(MotorSemantico):
    nome = "word2vec"

    def __init__(
        self,
        normalizador: Normalizador,
        limiares: dict[str, float] = LIMIARES_WORD2VEC,
        grupos: tuple[GrupoSemantico, ...] = GRUPOS,
        dimensoes: int = 64,
    ):
        self._normalizador = normalizador
        self._stemmer = RSLPStemmer()
        self._stopwords = {normalizador.normalizar(w) for w in stopwords.words("portuguese")}
        self._dimensoes = dimensoes
        self._modelo = self._treinar(grupos)
        super().__init__(limiares, grupos)

    def _stems(self, texto: str) -> list[str]:
        return [
            self._stemmer.stem(t)
            for t in self._normalizador.tokens(texto)
            if t not in self._stopwords
        ]

    def _treinar(self, grupos: tuple[GrupoSemantico, ...]) -> Word2Vec:
        documentos = []
        for grupo in grupos:
            for categoria in grupo.categorias:
                tokens: list[str] = []
                for semente in categoria.sementes:
                    tokens.extend(self._stems(semente))
                documentos.extend([tokens] * 8)
        return Word2Vec(
            documentos,
            vector_size=self._dimensoes,
            window=8,
            min_count=1,
            sg=1,
            epochs=200,
            seed=42,
            workers=1,
        )

    def _vetorizar(self, textos: list[str]) -> np.ndarray:
        vetores = np.zeros((len(textos), self._dimensoes), dtype=np.float32)
        for linha, texto in enumerate(textos):
            presentes = [
                self._modelo.wv[s] for s in self._stems(texto) if s in self._modelo.wv
            ]
            if not presentes:
                continue
            media = np.mean(presentes, axis=0)
            norma = np.linalg.norm(media)
            if norma > 0:
                vetores[linha] = media / norma
        return vetores


class MotorHibrid:
    nome = "hibrido"

    def __init__(self, transformer: MotorTransformer, word2vec: MotorWord2Vec):
        self._transformer = transformer
        self._word2vec = word2vec

    def classificar(self, trechos: list[str]) -> dict[str, tuple[Categoria, float]]:
        if not trechos:
            return {}
        res_t = self._transformer.classificar(trechos)
        res_w = self._word2vec.classificar(trechos)
        selecionados: dict[str, tuple[Categoria, float]] = {}
        for grupo in set(res_t) | set(res_w):
            if grupo in res_t and grupo in res_w:
                cat_t, score_t = res_t[grupo]
                cat_w, score_w = res_w[grupo]
                if cat_t.rotulo == cat_w.rotulo:
                    score = _PESO_TRANSFORMER * score_t + (1 - _PESO_TRANSFORMER) * score_w
                    selecionados[grupo] = (cat_t, round(score, 3))
                else:
                    selecionados[grupo] = (cat_t, score_t)
            elif grupo in res_t:
                selecionados[grupo] = res_t[grupo]
            else:
                selecionados[grupo] = res_w[grupo]
        return selecionados


class ConstrutorSql:
    _tabela = "people_images"
    _colunas = "id, nome, etnia, cor_cabelo, idade, label_etaria, caminho_imagem"

    def construir(self, kind: str, condicoes: list[str]) -> str:
        onde = f" WHERE {' AND '.join(condicoes)}" if condicoes else ""
        if kind == "count":
            return f"SELECT COUNT(*) AS total FROM {self._tabela}{onde}"
        return f"SELECT {self._colunas} FROM {self._tabela}{onde}"


@dataclass
class Resultado:
    motor: str
    kind: str
    condicoes: list[str]
    sql: str
    filtros: dict[str, dict]
    passos: list[dict] = field(default_factory=list)


class Pipeline:
    def __init__(self):
        self._normalizador = Normalizador()
        self._corretor = Corretor(self._normalizador)
        self._tipo = TipoConsulta()
        self._idade = IdadeNumerica()
        self._construtor = ConstrutorSql()
        motor_t = MotorTransformer(self._normalizador)
        motor_w = MotorWord2Vec(self._normalizador)
        motor_h = MotorHibrid(motor_t, motor_w)
        self._motores = {m.nome: m for m in (motor_t, motor_w, motor_h)}
        self._padrao = MotorHibrid.nome

    def motores(self) -> list[str]:
        return list(self._motores)

    def construtor(self) -> ConstrutorSql:
        return self._construtor

    def processar(self, texto: str, motor: str | None = None) -> Resultado:
        nome_motor = motor if motor in self._motores else self._padrao
        passos: list[dict] = []

        normalizado = self._normalizador.normalizar(texto)
        passos.append({"etapa": "normalizacao", "valor": normalizado})

        corrigido = self._corretor.corrigir(normalizado)
        passos.append({"etapa": "correcao_ortografica", "valor": corrigido})

        kind = self._tipo.detectar(self._normalizador.tokens(corrigido))
        passos.append({"etapa": "tipo_consulta", "valor": kind})

        condicao_idade = self._idade.condicao(corrigido)
        passos.append({"etapa": "idade_numerica", "valor": condicao_idade})

        trechos = self._normalizador.trechos(corrigido)
        passos.append({"etapa": "trechos", "valor": trechos})

        selecionados = self._motores[nome_motor].classificar(trechos)
        passos.append({
            "etapa": "correspondencia_semantica",
            "valor": {
                grupo: {"valor": categoria.rotulo, "score": round(score, 3)}
                for grupo, (categoria, score) in selecionados.items()
            },
        })

        condicoes: list[str] = []
        filtros: dict[str, dict] = {}
        for grupo, (categoria, score) in selecionados.items():
            if grupo == "faixa_etaria" and condicao_idade:
                continue
            condicoes.append(categoria.condicao)
            filtros[grupo] = {"valor": categoria.rotulo, "score": round(score, 3)}

        if condicao_idade:
            condicoes.append(condicao_idade)
            filtros["idade"] = {"valor": condicao_idade, "score": 1.0}

        sql = self._construtor.construir(kind, condicoes)
        passos.append({"etapa": "sql", "valor": sql})

        return Resultado(nome_motor, kind, condicoes, sql, filtros, passos)
