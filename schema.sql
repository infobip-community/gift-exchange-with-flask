CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    name TEXT NOT NULL,
    gift_bought INTEGER,
    verified INTEGER,
    giftee INT REFERENCES people(id)
);