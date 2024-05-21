from flask import Flask
import os
import psycopg
from dotenv import load_dotenv
import datetime

app = Flask(__name__)

def get_db_connection():
    conn = psycopg.connect(
        host="localhost",
        dbname="flask_db",
        user=os.getenv("DB_USERNAME"),
        password=os.getenv('DB_PASSWORD'))
    return conn

@app.get("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    print(books)
    print(int(datetime.datetime.combine(books[0][5], datetime.datetime.min.time()).timestamp()))
    response = [{'title': b[1], 'author': b[2], 'num_page': b[3], 'review': b[4], 'date_added': int(datetime.datetime.combine(b[5], datetime.datetime.min.time()).timestamp())} for b in books]
    cur.close()
    conn.close()
    return response, 200