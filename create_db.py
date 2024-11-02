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

# for product in products:
#     cursor.execute('INSERT INTO Products (title, description, price, photo) VALUES (?, ?, ?, ?)',
#                    (product[0], product[1], product[2], product[3]))

# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('John', 'male', 25, 180, 70)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Alice', 'female', 30, 165, 55)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Bob', 'male', 40, 175, 80)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Eva', 'female', 35, 170, 65)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Mike', 'male', 28, 185, 75)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Anna', 'female', 32, 160, 50)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Jack', 'male', 45, 178, 85)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Linda', 'female', 38, 168, 60)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Peter', 'male', 30, 182, 78)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Emily', 'female', 27, 163, 52)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Alex', 'male', 34, 177, 82)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Olivia', 'female', 29, 166, 57)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('David', 'male', 42, 180, 85)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Sophia', 'female', 33, 170, 62)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Kevin', 'male', 43, 175, 90)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Rachel', 'female', 31, 159, 49)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Daniel', 'male', 36, 178, 80)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Mia', 'female', 26, 162, 55)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('William', 'male', 38, 185, 88)")
# cursor.execute("INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES ('Victoria', 'female', 34, 168, 63)")

connection.commit()
connection.close()
