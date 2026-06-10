from __future__ import annotations

from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request, send_from_directory
from sqlalchemy import text

from database import engine
from semantic import Pipeline

app = Flask(__name__)
pipeline = Pipeline()


def _to_python(obj):
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def _linhas(conn, sql: str) -> list[dict]:
    return [
        {chave: _to_python(valor) for chave, valor in linha._mapping.items()}
        for linha in conn.execute(text(sql))
    ]


def _executar(resultado) -> dict | list:
    construtor = pipeline.construtor()
    with engine.connect() as conn:
        if resultado.kind == "count":
            total = _to_python(conn.execute(text(resultado.sql)).scalar())
            linhas = _linhas(conn, construtor.construir("rows", resultado.condicoes))
            return {"total": total, "rows": linhas}
        return _linhas(conn, resultado.sql)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", motores=pipeline.motores())


@app.route("/search", methods=["POST"])
def search():
    payload = request.get_json(silent=True) or {}
    consulta = (payload.get("query") or "").strip()
    if not consulta:
        return jsonify({"error": "Campo 'query' é obrigatório."}), 400

    resultado = pipeline.processar(consulta, payload.get("engine"))
    dados = _executar(resultado)

    return jsonify({
        "motor": resultado.motor,
        "sql": resultado.sql,
        "kind": resultado.kind,
        "filtros": resultado.filtros,
        "passos": resultado.passos,
        "resultado": dados,
    })


@app.route("/img/<path:filename>", methods=["GET"])
def serve_image(filename):
    img_dir = Path(app.static_folder) / "img"
    target = img_dir / filename
    if target.exists() and target.is_file():
        return send_from_directory(str(img_dir), filename)

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
