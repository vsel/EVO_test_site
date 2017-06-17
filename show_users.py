""" Special method for SELECT all users from database  """

from dbconnect import connection
import gc


def show_users():
    try:
        c, conn = connection()
        c.execute("SELECT username FROM users")
        rows = c.fetchall()
        c.close()
        conn.close()
        gc.collect()
        return rows
    except Exception as e:
        return(str(e))