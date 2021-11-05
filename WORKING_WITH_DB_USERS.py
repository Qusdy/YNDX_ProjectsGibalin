import sqlite3
from PIL import Image
import os

con = sqlite3.connect("bd_users.sqlite")

cur = con.cursor()

def is_there_that_name(login):
    if cur.execute("""SELECT name FROM name_password WHERE name = ?""",
                   (login,)).fetchall() == []:
        return False
    return True

def get_id(login):
    return cur.execute("""SELECT id FROM name_password WHERE name = ?""", (login,)).fetchall()[0][0]

def get_password(login):
    return str(cur.execute("""SELECT password FROM name_password WHERE name = ?""",
                       (login,)).fetchall()[0][0])

def get_picture(login):
    return str(cur.execute("""SELECT picture FROM name_password WHERE name = ?""",
                        (login,)).fetchall()[0][0])

def get_picture_format(login):
    return str(cur.execute("""SELECT picture_format FROM name_password WHERE name = ?""",
                       (login,)).fetchall()[0][0])

def registration_without_changing_photo(login, password):
    cur.execute("""INSERT into name_password(name, password) VALUES(?, ?)""", (login, password,))
    con.commit()

def registration_with_changing_photo(login, password, picture_format):
    cur.execute("""INSERT into name_password(name, password, picture, picture_format) VALUES(?, ?, ?, ?)""",
                (login, password, login, picture_format,))
    con.commit()

def updating_login(new_login, last_login):
    cur.execute("""UPDATE name_password SET name = ? WHERE name = ?""", (new_login, last_login,))
    con.commit()

def change_photo_in_db(new_login, new_format):
    cur.execute("""UPDATE name_password SET picture = ?, picture_format = ? WHERE name = ?""",
                (new_login, new_format, new_login,))
    con.commit()

def get_last_format(last_name):
    cur.execute("""SELECT picture_format FROM name_password WHERE name = ?""", (last_name,))

def saving_new_picture_name(new_name):
    cur.execute("""UPDATE name_password SET picture = ? WHERE name = ?""", (new_name, new_name,))

def get_format_from_picture(picture):
    return picture.split('.')[1]

def saving_new_profile_photo(photo_path, login):
    format = photo_path.split('.')[1]
    image = Image.open(photo_path)
    image.save(f'Фотографии пользователей/{login}.{format}')

def delete_account(login):
    id = get_id(login)
    table_1 = 'blocks_' + str(id)
    table_2 = 'goals_' + str(id)
    cur.execute(f"""DROP TABLE {table_1}""")
    cur.execute(f"""DROP TABLE {table_2}""")
    format = get_picture_format(login)
    try:
        os.remove(f'Фотографии пользователей/{login}.{format}')
    except FileNotFoundError:
        pass
    cur.execute("""UPDATE name_password SET is_deleted = True WHERE name = ?""", (login,))
    cur.execute("""DELETE FROM name_password WHERE is_deleted = True""")
    con.commit()

def create_tables(id):
    name_of_table1 = 'blocks_' + str(id)
    name_of_table2 = 'goals_' + str(id)
    cur.execute(f"""CREATE TABLE {name_of_table1}(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, deadline DATE, is_deleted BOOLEAN DEFAULT False)""")
    cur.execute(f"""CREATE TABLE {name_of_table2}(name STRING, bottom_goals STRING, deadline DATE, folder, is_complete BOOLEAN DEFAULT False,  is_deleted BOOLEAN DEFAULT False)""")
    con.commit()

