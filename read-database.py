import sqlite3

connection = sqlite3.connect("MyTable.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM men")

answer = cursor.fetchall()

for i in answer:
    print(i)