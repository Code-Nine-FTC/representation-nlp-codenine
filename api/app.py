"""
API Flask que expõe a busca semântica em /search e a UI em /.

Rotas:
  GET  /                    → renderiza a interface de chat (templates/index.html)
  POST /search              → recebe {"query": "..."}, devolve a SQL escolhida
                              e o resultado da execução no Postgres.
  GET  /img/<filename>      → serve uma imagem de api/static/img/, com
                              fallback para um SVG placeholder (silhueta +
                              nome) caso o arquivo não exista. Isso permite
                              que `caminho_imagem` no banco aponte para
                              /img/foo.jpg sem precisar das fotos reais
                              presentes para o demo.
"""

from __future__ import annotations

import re
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request, send_from_directory
from sqlalchemy import text

from database import engine
from nlp import find_best_intent
from queries import INTENTS

app = Flask(__name__)

# select para buscar a foto como as fotos tem o prefixo que a count do catalogo 
# entao faz o replace para a query de fotos
_COUNT_PREFIX = "SELECT COUNT(*) AS total FROM people_images"
_ROWS_BASE = (
    "SELECT id, nome, etnia, cor_cabelo, idade, "
    "label_etaria, caminho_imagem FROM people_images"
)

# Padrões para extrair intervalos etários numéricos da query antes do NLP.
_AGE_RANGE_PAT = re.compile(
    r"\b(\d{1,3})\s+[ae]\s+(\d{1,3})(?:\s+anos?)?", re.IGNORECASE
)
_AGE_ABOVE_PAT = re.compile(
    r"(?:acima|mais|partir)\s+de\s+(\d{1,3})\s*anos?", re.IGNORECASE
)


def _extract_age_range(text: str) -> tuple[str, str | None]:
    """
    aqui ele processa a idade pegando por min e max para montar a range
    """
    m = _AGE_RANGE_PAT.search(text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        lo, hi = min(a, b), max(a, b)
        clean = _AGE_RANGE_PAT.sub("", text).strip()
        return clean, f"idade BETWEEN {lo} AND {hi}"

    m = _AGE_ABOVE_PAT.search(text)
    if m:
        age = int(m.group(1))
        clean = _AGE_ABOVE_PAT.sub("", text).strip()
        return clean, f"idade > {age}"

    return text, None


def _to_python(obj):
    """Converte escalares numpy para tipos nativos json-serializáveis."""
    if hasattr(obj, "item"):
        return obj.item()
    return obj


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    payload = request.get_json(silent=True) or {}
    user_input = (payload.get("query") or "").strip()
    if not user_input:
        return jsonify({"error": "Campo 'query' é obrigatório."}), 400

    nlp_input, age_cond = _extract_age_range(user_input)

    intent_idx, score = find_best_intent(nlp_input or user_input)
    if intent_idx is None and not age_cond:
        return jsonify({
            "query_interpretada": None,
            "score": round(score, 3),
            "sql": None,
            "kind": None,
            "resultado": None,
            "mensagem": "Não encontrei uma intenção próxima o suficiente. Tente reformular.",
        })

    if intent_idx is not None:
        intent = INTENTS[intent_idx]
        sql = intent["sql"]
        kind = intent["kind"]
    else:
        sql = _ROWS_BASE
        kind = "rows"

    if age_cond:
        sql = sql + (" AND " if " WHERE " in sql else " WHERE ") + age_cond

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        if kind == "count":
            total = _to_python(result.scalar())
            rows_sql = sql.replace(_COUNT_PREFIX, _ROWS_BASE)
            rows_result = conn.execute(text(rows_sql))
            data = {
                "total": total,
                "rows": [
                    {key: _to_python(v) for key, v in row._mapping.items()}
                    for row in rows_result
                ],
            }
        else:
            data = [
                {key: _to_python(value) for key, value in row._mapping.items()}
                for row in result
            ]

    return jsonify({
        "query_interpretada": intent_idx,
        "score": round(score, 3),
        "sql": sql,
        "kind": kind,
        "resultado": data,
    })


@app.route("/img/<path:filename>", methods=["GET"])
def serve_image(filename):
    img_dir = Path(app.static_folder) / "img"
    target = img_dir / filename
    if target.exists() and target.is_file():
        return send_from_directory(str(img_dir), filename)

    # Sem arquivo no disco → devolve um SVG com silhueta + nome do arquivo,
    # útil para o demo enquanto não existem fotos reais.
    label = Path(filename).stem.replace("_", " ").replace("-", " ").title()
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" '
        'viewBox="0 0 240 240">'
        '<rect width="240" height="240" fill="#1f2937"/>'
        '<circle cx="120" cy="92" r="40" fill="#374151"/>'
        '<rect x="58" y="148" width="124" height="78" rx="38" fill="#374151"/>'
        f'<text x="120" y="218" font-family="system-ui,sans-serif" '
        f'font-size="14" fill="#cbd5e1" text-anchor="middle">{label}</text>'
        '</svg>'
    )
    return Response(svg, mimetype="image/svg+xml")


if __name__ == "__main__":
    app.run(debug=True)
