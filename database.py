import sqlite3

connection = sqlite3.connect('MyTable.db')

cursor = connection.cursor()

sql_command = '''CREATE TABLE men(
        stuff_number INTEGER PRIMARY KEY,
        fname VARCHAR(20),
        flastname VARCHAR(20),
        gender CHAR(5),
        joining GATE
);'''

if_tb_exists = "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'men' "
if not cursor.execute(if_tb_exists).fetchone():
    cursor.execute(sql_command)

data = """INSERT INTO men VALUES(
        25,
        "Andrey",
        'Goncharov',
        'male',        
        '2016-05-16'
)"""
cursor.execute(data)

connection.commit()
connection.close()