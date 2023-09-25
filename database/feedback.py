import mysql.connector
from database.database import connectToDB, log_event


def add_bug_report(user_id, bug):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = 'INSERT INTO bug_reports(user_id, bug) VALUES (%s, %s)'
        cursor.execute(query, (user_id, bug, ))
        conn.commit()
    except mysql.connector.Error as error:
        print("Error inserting the bug data:", error)
        log_event('Query error', f'Could not insert the bug data in the database: {error}')
    finally:
        cursor.close()
        conn.close()


def add_user_review(user_id, content):
    conn = connectToDB()
    cursor = conn.cursor()
    try:
        query = 'INSERT INTO user_reviews(user_id, content) VALUES (%s, %s)'
        cursor.execute(query, (user_id, content, ))
        conn.commit()
    except mysql.connector.Error as error:
        print("Error inserting the bug data:", error)
        log_event('Query error', f'Could not insert the review data in the database: {error}')
    finally:
        cursor.close()
        conn.close()




