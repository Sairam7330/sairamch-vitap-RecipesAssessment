import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_FILE = "recipes.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM recipes")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM recipes LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify({"data": data, "page": page, "limit": limit, "total": total})


@app.route("/api/recipes/search", methods=["GET"])
def search_recipes():
    title = request.args.get("title", "")
    min_rating = request.args.get("rating", "")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")

    if min_rating:
        query += " AND rating >= ?"
        params.append(float(min_rating))

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify({"data": data, "total": len(data)})


if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
