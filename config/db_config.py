import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="roundhouse.proxy.rlwy.net",
        user="root",
        password="CF4B2EG1h1Hf3h-3E4d46Ef5a-e1dfb4",
        database="railway",
        port="39493"
    )