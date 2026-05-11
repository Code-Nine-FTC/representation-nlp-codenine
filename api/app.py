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

from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request, send_from_directory
from sqlalchemy import text

from database import engine
from nlp import find_best_intent
from queries import INTENTS

app = Flask(__name__)


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

    intent_idx, score = find_best_intent(user_input)
    if intent_idx is None:
        return jsonify({
            "query_interpretada": None,
            "score": round(score, 3),
            "sql": None,
            "kind": None,
            "resultado": None,
            "mensagem": "Não encontrei uma intenção próxima o suficiente. Tente reformular.",
        })

    intent = INTENTS[intent_idx]
    sql = intent["sql"]
    kind = intent["kind"]

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        if kind == "count":
            data = _to_python(result.scalar())
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
