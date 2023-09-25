import mysql.connector

from database.database import connectToDB


def add_email(address, user_id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = 'INSERT INTO temp_emails(address, user_id) VALUES (%s, %s)'
        cursor.execute(query, (address, user_id, ))
        conn.commit()
    except mysql.connector.Error as error:
        print("Error inserting email:", error)
    finally:
        cursor.close()
        conn.close()


def get_mail_addr_count(user_id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = 'SELECT COUNT(*) FROM temp_emails WHERE user_id = %s AND ACTIVE = 1'
        cursor.execute(query, (user_id, ))
        count = cursor.fetchone()
        return count[0]
    except mysql.connector.Error as error:
        print("Error getting mail addresses:", error)
    finally:
        cursor.close()
        conn.close()


def get_mail_addr(user_id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = 'SELECT address FROM temp_emails WHERE user_id = %s AND ACTIVE = 1'
        cursor.execute(query, (user_id,))
        addresses = cursor.fetchall()
        return addresses
    except mysql.connector.Error as error:
        print("Error getting mail addresses:", error)
    finally:
        cursor.close()
        conn.close()


def delete_addr(user_id, email):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "UPDATE temp_emails SET active = 0 WHERE user_id = %s AND address = %s"
        cursor.execute(query, (user_id, email,))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error getting mail addresses:", error)
    finally:
        cursor.close()
        conn.close()