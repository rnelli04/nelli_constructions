import sqlite3

def add_area_column():
    connection = sqlite3.connect('nelli.db')
    cursor = connection.cursor()
    
    try:
        # Adds the new column without deleting your existing projects
        # We set a default of 'N/A' for any projects you already typed in
        cursor.execute("ALTER TABLE projects ADD COLUMN area TEXT DEFAULT 'N/A'")
        connection.commit()
        print("Success! The 'area' column was added to the database.")
    except sqlite3.OperationalError:
        print("Column might already exist, or there's a database lock.")
        
    connection.close()

if __name__ == '__main__':
    add_area_column()