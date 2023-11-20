import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="roundhouse.proxy.rlwy.net",
        user="root",
        password="cAgh-Cgc6CgHD1BBDbG6dD54feFGCH1d",
        database="railway",
        port="11673"
    )