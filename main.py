from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")  # Render provides this

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.get("/")
def read_root():
    return {"message": "IoT API running!"}

@app.get("/ingest")
def ingest_data(value: float):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sensor_data (value) VALUES (%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "Data ingested!"}
