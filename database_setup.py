import sqlite3

# Create database
conn = sqlite3.connect('vet_requests.db')
cursor = conn.cursor()

# Create table for vet requests
cursor.execute('''CREATE TABLE IF NOT EXISTS vet_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    time TEXT,
                    reason TEXT
                )''')

conn.commit()
conn.close()
