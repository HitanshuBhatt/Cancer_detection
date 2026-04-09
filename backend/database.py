import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root", # usually 'root'
        password="Root@123",
        database="LungCancer"
    )
    return connection