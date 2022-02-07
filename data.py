import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    # print(type(query))
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def set_new_user(connection, ident,  name, surname, patronymic):
    cursor = connection.cursor() 
    cursor.execute("insert into users(id, name, surname,patronymic) values (?,?,?,?)",
                   (ident, name, surname, patronymic))
    connection.commit()
    print('User was set sucsesful')


def find_chat_id(connection, ident): 
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE id=:id", {"id": ident})
    try:
        ident = cursor.fetchall()[0][0]
        result = 'DONE'
    except:
    	result = 'ERROR'
    return result


def read_all(connection, ident): 
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=:id", {"id": ident})
    result = cursor.fetchall()
    return result


def read_all_by_name(connection, ident): 
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE surname=:id", {"id": ident})
    result = cursor.fetchall()
    return result


def read_name(connection, ident): 
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM users WHERE id=:id", {"id": ident})
    result = cursor.fetchall()[0][0]
    return result


def read_patronymic(connection, ident): 
    cursor = connection.cursor()
    cursor.execute("SELECT patronymic FROM users WHERE id=:id", {"id": ident})
    result = cursor.fetchall()[0][0]
    return result


def read_fio(connection, ident):
    cursor = connection.cursor()
    cursor.execute("SELECT surname, name, patronymic FROM users WHERE id=:id", {"id": ident})
    fio = cursor.fetchall()[0]
    result = str(fio[0]) + ' ' + str(fio[1])[0] +'.'+str(fio[2])[0]+'.'
    return result


def delete_user(connection, ident):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id=:id", {"id": ident})
        result = 'DONE'
    except:
        result = 'ERROR'
    return result


def read_buts(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM buttons ")
    result = cursor.fetchall()
    return result


def update_place(connection,ident, new_message): 
    cursor = connection.cursor()
    cursor.execute("UPDATE buttons SET place=:new_value WHERE id=:id",
                   {"id": ident, "new_value": new_message})
    print('Message was update')
    connection.commit()


def update_small_place(connection,ident, new_message): 
    cursor = connection.cursor()
    cursor.execute("UPDATE buttons SET abr_place=:new_value WHERE id=:id",
                   {"id": ident, "new_value": new_message})
    print('Message was update')
    connection.commit()


def delete_button(connection, ident):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM buttons WHERE id=:id", {"id": ident})
    return 


def new_button(connection):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO buttons(place, abr_place) VALUES ('New_place', 'New_place_small')") 
    return 


def find_place(connection, place):
    cursor = connection.cursor()
    cursor.execute("SELECT abr_place FROM buttons WHERE place=:arg",
                   {"arg": place})
    result = cursor.fetchall()[0][0]
    return result


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")





