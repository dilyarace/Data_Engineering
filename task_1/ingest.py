import re
import json
import sqlite3

# Read the file
with open("task1_d.json", "r", encoding="utf-8") as f:
    content = f.read()

# Convert the file to JSON format
content = re.sub(r':(\w+)=>', r'"\1":', content)
books = json.loads(content)

# Connect to the database
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Create a table for raw data
cursor.execute("""
    CREATE TABLE books (
        id        TEXT,
        title     TEXT,
        author    TEXT,
        genre     TEXT,
        publisher TEXT,
        year      INTEGER,
        price_raw TEXT
    )
""")

# Insert the data
for book in books:
    cursor.execute(
        "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            str(book["id"]),
            book["title"],
            book.get("author"),
            book.get("genre"),
            book.get("publisher"),
            book.get("year"),
            book["price"]
        )
    )

conn.commit()

# Create the final table via SQL
cursor.execute("""
    CREATE TABLE summary AS
    SELECT
        year AS publication_year,
        COUNT(*) AS book_count,
        ROUND(AVG(
            CASE
                WHEN price_raw LIKE '$%'
                    THEN CAST(REPLACE(price_raw, '$', '') AS REAL)
                WHEN price_raw LIKE '€%'
                    THEN CAST(REPLACE(price_raw, '€', '') AS REAL) * 1.2
            END
        ), 2) AS average_price_usd
    FROM books
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year
""")

conn.commit()
conn.close()

print("Done!")