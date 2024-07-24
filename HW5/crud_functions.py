import sqlite3


class DataError(Exception):
    pass


def initiate_db():
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
                   'username TEXT NOT NULL,'
                   'email TEXT NOT NULL,'
                   'age INTEGER NOT NULL,'
                   'balance INTEGER NOT NULL)')

    cursor.execute('CREATE TABLE IF NOT EXISTS Users_par('
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

    return connection, cursor


def get_all_products():
    connection, cursor = initiate_db()
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def add_user(username, email, age, balance=1000):
    connection, cursor = initiate_db()
    check_user = cursor.execute(f'SELECT * FROM Users WHERE username = "{username}"')
    if not check_user.fetchone():
        cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                       (username, email, age, balance))
        connection.commit()
        connection.close()
    else:
        raise DataError(f'Пользователь {username} уже есть в базе данных.')


def is_included(username):
    connection, cursor = initiate_db()
    check_user = cursor.execute(f'SELECT * FROM Users WHERE username = "{username}"')
    result = check_user.fetchone() != None
    connection.commit()
    connection.close()
    return result


def set_user_info(first_name, gender=None, age=None, growth=None, weight=None):
    connection, cursor = initiate_db()
    cursor.execute('INSERT INTO Users_par (first_name, gender, age, growth, weight) VALUES (?, ?, ?, ?, ?)',
                   (first_name, gender, age, growth, weight))
    connection.commit()
    connection.close()
