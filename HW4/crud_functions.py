import sqlite3

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

    # connection.commit()
    # connection.close()


def get_all_products():
    connection, cursor = initiate_db()
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def set_user_info(first_name, gender=None, age=None, growth=None, weight=None):
    connection, cursor = initiate_db()
    # check_user = cursor.execute('SELECT * FROM Users WHERE first_name = ?', (first_name))
    # if not check_user.fetchone():
    cursor.execute('INSERT INTO Users (first_name, gender, age, growth, weight) VALUES (?, ?, ?, ?, ?)',
                   (first_name, gender, age, growth, weight))
    # else:
    #     cursor.execute('UPDATE Users SET (gender = ?, age = ?, growth = ?, weight = ?) '
    #                    'WHERE first_name = ?', (gender, age, growth, weight, first_name))
    connection.commit()
    connection.close()


