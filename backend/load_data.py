import json
import os
import sqlite3

DB_NAME = "recipes.db"
JSON_FILE = "recipes.json"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cuisine TEXT,
        title TEXT,
        rating REAL,
        prep_time INTEGER,
        cook_time INTEGER,
        total_time INTEGER,
        description TEXT,
        nutrients TEXT,
        serves TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_data():
    if not os.path.exists(JSON_FILE):
        print(f"❌ {JSON_FILE} not found!")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔑 FIX: Ensure we only take dictionary values, not keys
    if isinstance(data, dict):
        recipes = list(data.values())
    elif isinstance(data, list):
        recipes = data
    else:
        print("❌ Unknown JSON format!")
        return

    print(f"Loading {len(recipes)} recipes...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for recipe in recipes:
        if not isinstance(recipe, dict):
            continue  # skip if not a dictionary

        cursor.execute("""
            INSERT INTO recipes (
                cuisine, title, rating, prep_time, cook_time, total_time,
                description, nutrients, serves
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            recipe.get("cuisine"),
            recipe.get("title"),
            None if recipe.get("rating") in [
                "NaN", None] else recipe.get("rating"),
            None if recipe.get("prep_time") in [
                "NaN", None] else recipe.get("prep_time"),
            None if recipe.get("cook_time") in [
                "NaN", None] else recipe.get("cook_time"),
            None if recipe.get("total_time") in [
                "NaN", None] else recipe.get("total_time"),
            recipe.get("description"),
            json.dumps(recipe.get("nutrients", {})),
            recipe.get("serves")
        ))

    conn.commit()
    conn.close()
    print("✅ Data inserted successfully into SQLite (recipes.db)")


if __name__ == "__main__":
    create_table()
    insert_data()
