""" Special method for CONNECTING to the database  """
import MySQLdb


def connection():
    conn = MySQLdb.connect(host='some host', user='admin username', passwd='password for db', db='name of db')
    c = conn.cursor()

    return c, conn
