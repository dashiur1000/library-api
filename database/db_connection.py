import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3309,
    user="root",
    password="secret",
    database="library_db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(50) UNIQUE,
author VARCHAR(50) UNIQUE,
genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
is_available BOOLEAN DEFAULT TRUE,
borrowed_by_number_id INT DEFAULT NULL
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT FALSE NOT NULL,
    total_borrows INT NOT NULL)
"""
)

conn.commit()

cursor.close()
conn.close()