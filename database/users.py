import mysql.connector

from database.database import connectToDB


def addUser(t_id, username, lang_code, f_name, l_name):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users(teleg_id, first_name, last_name, username, lang_code) VALUES(%s, %s, %s, %s, %s)"
        cursor.execute(query, (t_id, f_name, l_name, username, lang_code))
        conn.commit()
    except mysql.connector.Error as error:
        print("Error adding user:", error)
    finally:
        cursor.close()
        conn.close()


def checkUserInDB(id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM users WHERE teleg_id = %s"
        cursor.execute(query, (id,))
        res = cursor.fetchone()
    except mysql.connector.Error as error:
        print("Error checking user in the database:", error)
        res = None
    finally:
        cursor.close()
        conn.close()
    if res is not None:
        return True
    return False


def get_user_info(t_id):
    conn = connectToDB()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE teleg_id = %s"
        cursor.execute(query, (t_id,))
        user_info = cursor.fetchone()
    except mysql.connector.Error as error:
        print("Error getting user info:", error)
        user_info = None
    finally:
        cursor.close()
        conn.close()
    return user_info