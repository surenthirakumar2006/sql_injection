import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the 'users' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')

# Insert the required user if not already present
cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'baymax@gmail.com'")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users (username, password) VALUES ('baymax@gmail.com', 'anypassword')")

conn.commit()
conn.close()
print("Database setup complete!")
