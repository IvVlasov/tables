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
    cursor.execute("insert into users(id, name, surname,patronymic) values (?,?,?,?)", (ident, name, surname, patronymic))
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

##############################BUTTONS#######################################
def read_buts(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM buttons ")
    result = cursor.fetchall()
    return result

def update_place(connection,ident, new_message): 
    cursor = connection.cursor()
    cursor.execute("UPDATE buttons SET place=:new_value WHERE id=:id", {"id": ident, "new_value": new_message})
    print('Message was update')
    connection.commit()

def update_small_place(connection,ident, new_message): 
    cursor = connection.cursor()
    cursor.execute("UPDATE buttons SET abr_place=:new_value WHERE id=:id", {"id": ident, "new_value": new_message})
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
    cursor.execute("SELECT abr_place FROM buttons WHERE place=:arg", {"arg": place})
    result = cursor.fetchall()[0][0]
    return result

# ######################################################## READ ##################################################
# def read_companion(connection, ident): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT companion FROM users WHERE chatID=:id", {"id": ident})
#     result = cursor.fetchall()[0][0]
#     return result

# def read_subscribe(connection, ident): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT subscribe FROM users WHERE chatID=:id", {"id": ident})
#     result = cursor.fetchall()[0][0]
#     return result

# # def read_all(connection): 
# #     cursor = connection.cursor()
# #     cursor.execute("SELECT chatID FROM users")
# #     result = cursor.fetchall()
# #     return result
# # # 
# def read_status(connection, ident): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT status FROM users WHERE chatID=:id", {"id": ident})
#     result = cursor.fetchall()[0][0]
#     return result

# def read_data(connection, ident): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT dateReg FROM users WHERE chatID=:id", {"id": ident})
#     result = cursor.fetchall()[0][0]
#     return result

# def read_gender(connection, ident): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT gender FROM users WHERE chatID=:id", {"id": ident})
#     result = cursor.fetchall()[0][0]
#     return result


# ######################################################## UPDATE ##################################################
# def update_message(connection,ident, new_message): 
#     cursor = connection.cursor()
#     cursor.execute("UPDATE users SET message=:new_value WHERE chatID=:id", {"id": ident, "new_value": new_message})
#     print('Message was update')
#     connection.commit()

# def update_companion(connection,ident, new_value): 
#     cursor = connection.cursor()
#     cursor.execute("UPDATE users SET companion=:new_value WHERE chatID=:id", {"id": ident, "new_value": new_value})
#     print('Message was update')
#     connection.commit()

# def update_status(connection,ident,value): 
#     cursor = connection.cursor()
#     cursor.execute("UPDATE users SET status=:new_value WHERE chatID=:id", {"id": ident, "new_value": value})
#     connection.commit()

# def update_date(connection,ident,value): 
#     cursor = connection.cursor()
#     cursor.execute("UPDATE users SET dateReg=:new_value WHERE chatID=:id", {"id": ident, "new_value": value})
#     connection.commit()


# def update_subscribe(connection,ident,value): 
#     cursor = connection.cursor()
#     cursor.execute("UPDATE users SET subscribe=:new_value WHERE chatID=:id", {"id": ident, "new_value": value})
#     connection.commit()

# ######################################################## SEARCH ############################################

# def search_active_status(connection,ident, value): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT chatID FROM users WHERE status=:value AND chatID!=:id", {"value": value, "id":ident})
#     result = cursor.fetchall()
#     return result

# def search_active_gender(connection,ident, gender_to_find, value): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT chatID FROM users WHERE status=:value AND chatID!=:id AND gender=:pol", {"value": value, "id":ident, "pol": gender_to_find})
#     result = cursor.fetchall()
#     return result

# def search_active_man(connection,ident, gender_to_find): 
#     cursor = connection.cursor()
#     cursor.execute("SELECT chatID FROM users WHERE  chatID!=:id AND genderFind=:pol", {"value": 1, "id":ident, "pol": gender_to_find})
#     result = cursor.fetchall()
#     return result

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")





