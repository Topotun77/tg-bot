# Домашнее задание по теме "Выбор элементов и функции в SQL запросах"
# Цель: научится использовать функции внутри запросов языка SQL и использовать их в решении задачи.
#
# Задача "Средний баланс пользователя":
# Для решения этой задачи вам понадобится решение предыдущей.
# Для решения необходимо дополнить существующий код:
# 1. Удалите из базы данных not_telegram.db запись с id = 6.
# 2. Подсчитать общее количество записей.
# 3. Посчитать сумму всех балансов.
# 4. Вывести в консоль средний баланс всех пользователя.

import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Users('
               'id INTEGER PRIMARY KEY,'
               'username TEXY NOT NULL,'
               'email TEXT NOT NULL,'
               'age INTEGER,'
               'balance INTEGER NOT NULL)')

for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', i * 10, 1000))

for i in range(1,11,2):
    cursor.execute('UPDATE Users SET balance = ? WHERE username = ?',
                   (500, f'User{i}'))

for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE username = ?',
                   (f'User{i}',))

cursor.execute('SELECT * FROM Users WHERE age != ?', (60,))
result = cursor.fetchall()
for user in result:
    print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

cursor.execute('DELETE FROM Users WHERE id = ?',
                   (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
count = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
balance_sum = cursor.fetchone()[0]
cursor.execute('SELECT AVG(balance) FROM Users')
balance_avg = cursor.fetchone()[0]
balance_avg2 = balance_sum / count

print(f'Средний баланс, подсчитанный через запрос AVG: {balance_avg}',
      f'Средний баланс, подсчитанный делением: {balance_avg2}', sep='\n')

connection.commit()
connection.close()
