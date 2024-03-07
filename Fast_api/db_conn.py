import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Create books table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        publication_year INTEGER
    )
''')

# Create reviews table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        book_id INTEGER,
        text TEXT,
        rating INTEGER,
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("SQLite database and tables created successfully.")
