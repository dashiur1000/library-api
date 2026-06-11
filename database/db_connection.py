import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="mydatabase"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(50) UNIQUE,
author VARCHAR(50) UNIQUE,
genre VARCHAR(255) ["Fiction", "Non-Fiction", "Science", "History", "Other"],
is_available BOOLEAN,
)
""")