import mysql.connector


def connectToDB():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        port="4000",
        database="charleedb"
    )


def update_user_preferences(user_id, preferences):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "UPDATE users SET preferences = %s WHERE teleg_id = %s"
        cursor.execute(query, (preferences, user_id))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error updating preferences:", error)
        return False
    finally:
        cursor.close()
        conn.close()





def log_event(ev_type, ev_description):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = 'INSERT INTO logs(event_type, event_description) VALUES (%s, %s)'
        cursor.execute(query, (ev_type, ev_description,))
        conn.commit()
    except mysql.connector.Error as error:
        print("Error logging event:", error)
    finally:
        cursor.close()
        conn.close()



