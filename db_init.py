import pandas as pd
import sqlite3

def initialize_database():
    conn = sqlite3.connect('client_queries.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT,
        role TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS queries (
        query_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mail_id TEXT,
        mobile_number TEXT,
        query_heading TEXT,
        query_description TEXT,
        status TEXT,
        query_created_time TEXT,
        query_closed_time TEXT
    )''')

    df = pd.read_csv('synthetic_client_queries.csv')
    df.to_sql('queries', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
