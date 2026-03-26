import sqlite3 as sql

# SQL --

conn = sql.connect("test.db")
conn.row_factory = sql.Row
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

#cursor.execute("DELETE FROM test WHERE id = ?", (2,))
#cursor.execute("INSERT INTO test (title) VALUES (?)", ("testing",))
#cursor.execute("SELECT * FROM test")

conn.commit()
conn.close()