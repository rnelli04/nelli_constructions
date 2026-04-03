import sqlite3

def create_database():
    connection = sqlite3.connect('nelli.db')
    cursor = connection.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS projects")
    
    create_table_query = """
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        image_file TEXT NOT NULL
    );
    """
    
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()
    
    print("Success! Database 'nelli.db' recreated with the image_file column.")

if __name__ == '__main__':
    create_database()