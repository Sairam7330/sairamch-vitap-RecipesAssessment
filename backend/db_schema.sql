DROP TABLE IF EXISTS recipes;

CREATE TABLE recipes (
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
);
