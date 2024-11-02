import sqlite3

connection = sqlite3.connect('tg_data.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS Products('
               'id INTEGER PRIMARY KEY,'
               'title TEXT NOT NULL,'
               'description TEXT,'
               'price INTEGER NOT NULL,'
               'photo TEXT)')

cursor.execute('CREATE TABLE IF NOT EXISTS Users('
               'id INTEGER PRIMARY KEY,'
               'first_name TEXT NOT NULL,'
               'gender TEXT,'
               'age INTEGER,'
               'growth INTEGER,'
               'weight INTEGER)')

cursor.execute('CREATE TABLE IF NOT EXISTS Buy('
               'id INTEGER PRIMARY KEY,'
               'first_name TEXT NOT NULL,'
               'data TEXT NOT NULL,'
               'product TEXT NOT NULL,'
               'price INTEGER NOT NULL)')

cursor.execute('CREATE INDEX IF NOT EXISTS ind_name ON Buy (first_name)')
cursor.execute('CREATE INDEX IF NOT EXISTS ind_prod ON Buy (product)')

products = [
    ['Лот #001', 'Очень бюджетный вариант', 199, 'image/006.JPG'],
    ['Лот #002', 'Разновидность бюджетного варианта', 299, 'image/003.JPG'],
    ['Лот #003', 'Инструкция для самостоятельной реализации на базе экранов Nextion', 2_999, 'image/009.JPG'],
    ['Лот #004', 'Высокоинтеллектуальное решение на базе ИИ', 29_999, 'image/007.JPG'],
    ['Лот #005', 'Высокоинтеллектуальное решение на базе ИИ с дактилоскопическим анализом состояния здоровья',
     69_999, 'image/008.JPG'],
    ['Лот #006', 'Самое эффективное решение по невероятно низкой цене', 9, 'image/010.JPG']
]

for product in products:
    cursor.execute('INSERT INTO Products (title, description, price, photo) VALUES (?, ?, ?, ?)',
                   (product[0], product[1], product[2], product[3]))

connection.commit()
connection.close()
