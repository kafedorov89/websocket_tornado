import MySQLdb
from torndb import Connection

db = None
ip_address = '127.0.0.1'
db_name = 'electrolab'
db_user = 'django'
db_password = '31415926'

def GetConnection():
    return Connection(ip_address, db_name, user = db_user, password = db_password)