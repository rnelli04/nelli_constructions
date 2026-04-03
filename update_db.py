import sqlite3

def add_messages_table():
    connection = sqlite3.connect('nelli.db')
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)
    
    connection.commit()
    connection.close()
    print("Success! The 'messages' table has been added to your database.")

if __name__ == '__main__':
    add_messages_table()