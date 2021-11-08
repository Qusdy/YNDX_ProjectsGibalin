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
    cur.execute(f"""CREATE TABLE {name_of_table2}(name STRING, deadline DATE, folder, is_complete BOOLEAN DEFAULT False,  is_deleted BOOLEAN DEFAULT False)""")
    con.commit()

def creating_block_in_db(name_of_table, name, date):
    cur.execute(f'INSERT into {name_of_table}(name, deadline) VALUES(?, ?)', (name, date,))
    con.commit()

def creating_goal_in_db(table_name, name, date, folder):
    cur.execute(f'INSERT into {table_name}(name, deadline, folder) VALUES(?, ?, ?)', (name, date, folder,))
    con.commit()

def get_all_dates(table_goals, table_blocks):
    dates = set()
    for el in get_list(search_blocks_dates(table_blocks)):
        dates.add(el)
    for el in get_list(search_goals_dates(table_goals)):
        dates.add(el)
    return sorted(list(dates))

def get_list(list_with_kort):
    result_list = []
    for el in list_with_kort:
        result_list.append(el[0])
    return result_list

def get_dates_without_repeating(list_with_dates):
    return sorted(list(set(list_with_dates)))

def search_blocks_dates(name_of_table):
    return cur.execute(f'SELECT deadline FROM {name_of_table} ORDER BY deadline ASC').fetchall()

def search_goals_dates(name_of_table):
    return cur.execute(f'SELECT deadline FROM {name_of_table} WHERE folder is NULL ORDER BY deadline ASC').fetchall()

def search_goals_in_block_dates(name_of_table, id):
    return cur.execute(f'SELECT deadline FROM {name_of_table} WHERE folder = ? ORDER BY deadline', (id,)).fetchall()

def get_all_objects(table_goals, table_blocks, date):
    all_objects = []
    for el in get_list(get_goals_on_this_date(table_goals, date)):
        all_objects.append(el)
    for el in get_list(get_blocks_on_this_date(table_blocks, date)):
        all_objects.append(el)
    return all_objects

def get_goals_on_this_date(table_goals, date):
    return cur.execute(f'SELECT name FROM {table_goals} WHERE deadline = ? AND folder is NULL', (date,)).fetchall()

def get_blocks_on_this_date(table_blocks, date):
    return cur.execute(f'SELECT name FROM {table_blocks} WHERE deadline = ?', (date,)).fetchall()

def get_goals_in_block_at_this_date(table_name, id, date):
    return cur.execute(f'SELECT name FROM {table_name} WHERE deadline = ? AND folder = ?', (date, id,)).fetchall()

def is_there_that_folder_name(name_of_table, name):
    if cur.execute(f'SELECT id FROM {name_of_table} WHERE name = ?', (name,)).fetchall() == []:
        return False
    return True

def get_all_blocks(name_of_table):
    return cur.execute(f'SELECT name FROM {name_of_table}').fetchall()

def get_block_id(name_of_table, name_of_block):
    return cur.execute(f'SELECT id FROM {name_of_table} WHERE name = ?', (name_of_block,)).fetchall()[0][0]

def get_date(name_of_table, name_of_object):
    return '.'.join(cur.execute(f'SELECT deadline FROM {name_of_table} WHERE name = ?', (name_of_object,)).fetchall()[0][0].split('-')[::-1])

def remove_goal_from_block_db(goal_to_remove, block_id, table_name):
    cur.execute(f'UPDATE {table_name} SET is_deleted = True WHERE folder = ? AND name = ?', (block_id, goal_to_remove,))
    cur.execute(f'DELETE FROM {table_name} WHERE is_deleted = True')
    con.commit()

def delete_block(name_of_table, block_name):
    cur.execute(f'UPDATE {name_of_table} SET is_deleted = True WHERE name = ?', (block_name,))
    cur.execute(f'DELETE FROM {name_of_table} WHERE is_deleted = True')
    con.commit()