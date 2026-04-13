# Task 1 — Data Ingestion & SQL Transformation
An internship assignment focused on data parsing, database ingestion, and SQL-based transformation using Python and SQLite.

## Problem Statement
Given a file `task1_d.json` (which is not valid JSON), the goal was to:
1. Parse the file and fix the format to make it readable
2. Load the raw data into a relational database table `books`
3. Use SQL to produce a summary table with the following fields:
   - `publication_year` — year the book was published
   - `book_count` — number of books published that year
   - `average_price_usd` — average price in USD, rounded to cents (€1 = $1.2)

## What I Learned

### File Format — Ruby Hash
The file looked like JSON but used Ruby Hash syntax:
```ruby
{:id=>123, :title=>"Some Book", :year=>2010, :price=>"€5.99"}
```
Valid JSON looks like this:
```json
{"id": 123, "title": "Some Book", "year": 2010, "price": "€5.99"}
```
Two differences: keys use `:key=>` instead of `"key":`. One regex line fixes this:
```python
content = re.sub(r':(\w+)=>', r'"\1":', content)
```
What this does:
- Find any pattern like `:word=>`
- Replace it with `"word":`
- After that, `json.loads()` can parse it normally

### Relational Database & SQLite
A relational database stores data in tables with rows and columns — like a spreadsheet, but queryable with SQL.

**SQLite** is a lightweight database that lives in a single `.db` file. It is built into Python — no installation needed:
```python
import sqlite3
conn = sqlite3.connect("books.db")  # creates the file
cursor = conn.cursor()
```

### Raw vs Transformed Data
The raw data is loaded into the database exactly as it came from the file — prices are stored as strings like `"$12.50"` or `"€5.99"`. No processing happens in Python. This is intentional: the task requires that all transformation logic lives inside the database as SQL.

### SQL Transformation
The summary table is built entirely with SQL. Key concepts used:

**LIKE** — checks if a string matches a pattern:
```sql
price_raw LIKE '$%'   -- starts with $
price_raw LIKE '€%'   -- starts with €
```

**REPLACE** — removes a character from a string:
```sql
REPLACE(price_raw, '$', '')   -- "$12.50" → "12.50"
```

**CAST** — converts a string to a number:
```sql
CAST('12.50' AS REAL)   -- "12.50" → 12.50
```

**CASE WHEN** — conditional logic (like if/else):
```sql
CASE
    WHEN price_raw LIKE '$%' THEN CAST(REPLACE(price_raw, '$', '') AS REAL)
    WHEN price_raw LIKE '€%' THEN CAST(REPLACE(price_raw, '€', '') AS REAL) * 1.2
END
```

**AVG + GROUP BY** — average per group:
```sql
AVG(...) ... GROUP BY year   -- calculates average price separately for each year
```

**ROUND(..., 2)** — rounds to 2 decimal places (cents).

## Pipeline Overview
```
task1_d.json (Ruby Hash format)
        │
        ▼  regex fix in Python
valid JSON → list of dicts
        │
        ▼  INSERT in Python
table: books (raw data, 5003 rows)
        │
        ▼  CREATE TABLE ... AS SELECT in SQL
table: summary (49 rows, one per year)
        │
        └── publication_year
        └── book_count
        └── average_price_usd
```

## Common Pitfalls
| Mistake | Why it matters |
|---|---|
| Converting prices in Python instead of SQL | Violates the requirement — transformation must be inside the database |
| Storing `id` as INTEGER | The IDs in this file are too large for SQLite INTEGER — use TEXT |
| Not deleting `books.db` before re-running | SQLite throws an error if the table already exists |
| Forgetting `conn.commit()` | Changes are not saved to the file without it |
| Using `LIKE '€%'` without checking encoding | The `€` symbol is multi-byte in UTF-8 — works in SQLite but worth being aware of |

## Stack
- **Language:** Python 3
- **Database:** SQLite (built-in)
- **Libraries:** `re`, `json`, `sqlite3` — no external dependencies
