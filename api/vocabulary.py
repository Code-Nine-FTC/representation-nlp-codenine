from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Categoria:
    rotulo: str
    condicao: str
    sementes: tuple[str, ...]


@dataclass(frozen=True)
class GrupoSemantico:
    nome: str
    categorias: tuple[Categoria, ...]


ETNIA = GrupoSemantico(
    "etnia",
    (
        Categoria("branca", "etnia = 'branca'", (
            "pessoa branca", "etnia branca", "pessoa de pele branca", "caucasiano",
        )),
        Categoria("negra", "etnia = 'negra'", (
            "pessoa negra", "etnia negra", "pessoa de pele negra",
            "afrodescendente", "pessoa preta",
        )),
        Categoria("parda", "etnia = 'parda'", (
            "pessoa parda", "etnia parda", "pessoa morena", "mulato",
        )),
        Categoria("asiatica", "etnia = 'asiatica'", (
            "pessoa asiática", "etnia asiática", "pessoa oriental",
            "descendente de japonês",
        )),
        Categoria("indigena", "etnia = 'indigena'", (
            "pessoa indígena", "etnia indígena", "índio", "nativo",
        )),
    ),
)


COR_CABELO = GrupoSemantico(
    "cor_cabelo",
    (
        Categoria("loiro", "cor_cabelo = 'loiro'", (
            "loiro", "loira", "cabelo loiro", "cabelo louro", "cabelos dourados",
        )),
        Categoria("preto", "cor_cabelo = 'preto'", (
            "preto", "cabelo preto", "cabelo escuro", "cabelos pretos",
        )),
        Categoria("castanho", "cor_cabelo = 'castanho'", (
            "castanho", "cabelo castanho", "cabelo marrom", "cabelos castanhos",
        )),
        Categoria("ruivo", "cor_cabelo = 'ruivo'", (
            "ruivo", "ruiva", "cabelo ruivo", "cabelos ruivos", "cabelo avermelhado",
        )),
        Categoria("grisalho", "cor_cabelo = 'grisalho'", (
            "grisalho", "cabelo grisalho", "cabelo cinza",
            "cabelo prateado", "cabelos grisalhos",
        )),
    ),
)


FAIXA_ETARIA = GrupoSemantico(
    "faixa_etaria",
    (
        Categoria("bebê", "idade <= 5", (
            "bebê", "neném", "recém-nascido", "bebezinho",
        )),
        Categoria("criança", "idade BETWEEN 6 AND 12", (
            "criança", "menino", "menina", "criança pequena",
        )),
        Categoria("adolescente", "idade BETWEEN 13 AND 17", (
            "adolescente", "garoto adolescente", "menina adolescente",
        )),
        Categoria("jovem", "idade BETWEEN 18 AND 25", (
            "jovem", "jovem adulto", "rapaz", "moça",
        )),
        Categoria("adulto", "idade BETWEEN 26 AND 40", (
            "adulto", "pessoa adulta",
        )),
        Categoria("meia-idade", "idade BETWEEN 41 AND 60", (
            "pessoa de meia idade", "meia-idade", "adulto mais velho",
        )),
        Categoria("idoso", "idade > 60", (
            "idoso", "pessoa idosa", "velho", "ancião", "terceira idade", "vovô",
        )),
    ),
)


GRUPOS: tuple[GrupoSemantico, ...] = (ETNIA, COR_CABELO, FAIXA_ETARIA)
