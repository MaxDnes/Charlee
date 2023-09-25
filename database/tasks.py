import mysql.connector
from database.database import connectToDB


def get_tasks(user_id, active):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM tasks WHERE user_id = %s AND status = %s AND active = 1"
        cursor.execute(query, (user_id, active))
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as error:
        print("Error marking task as completed:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def get_task(id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM tasks WHERE id = %s AND active = 1"
        cursor.execute(query, (id, ))
        tasks = cursor.fetchone()
        return tasks
    except mysql.connector.Error as error:
        print("Error marking task as completed:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def complete_task(id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "UPDATE tasks SET status = 'done', completed_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (id, ))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error marking task as completed:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def delete_task(id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "UPDATE tasks SET active = 0 WHERE id = %s"
        cursor.execute(query, (id, ))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error deleting task:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def add_user_task(user_id, task_content):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = 'INSERT INTO tasks(user_id, task) VALUES (%s, %s)'
        cursor.execute(query, (user_id, task_content))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error adding user task:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def mark_task_completed(user_id, task_id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "UPDATE tasks SET status = 'done' WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, task_id,))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error marking task as completed:", error)
        return False
    finally:
        cursor.close()
        conn.close()


def set_due_date(task_id, date):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "UPDATE tasks SET due_date = %s WHERE id = %s"
        cursor.execute(query, (date, task_id,))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error getting mail addresses:", error)
    finally:
        cursor.close()
        conn.close()


def set_due_time(task_id, hour, minutes):
    conn = connectToDB()
    cursor = conn.cursor()
    time = f"{hour}:{minutes}:00"
    try:
        query = "UPDATE tasks SET due_time = %s WHERE id = %s"
        cursor.execute(query, (time, task_id,))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error getting mail addresses:", error)
    finally:
        cursor.close()
        conn.close()


def remove_due_date(task_id):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = "UPDATE tasks SET due_date = %s WHERE id = %s"
        cursor.execute(query, (None, task_id, ))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        print("Error getting mail addresses:", error)
    finally:
        cursor.close()
        conn.close()
