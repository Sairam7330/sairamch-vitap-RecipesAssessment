import sqlite3

conn = sqlite3.connect("recipes.db")
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Count rows in recipes table
cursor.execute("SELECT COUNT(*) FROM recipes;")
print("Total recipes:", cursor.fetchone()[0])

# Show some sample rows
cursor.execute("SELECT id, title, cuisine, rating FROM recipes LIMIT 5;")
for row in cursor.fetchall():
    print(row)

conn.close()
