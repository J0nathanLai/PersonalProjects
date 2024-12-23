import psycopg2
from pprint import pprint as pp
from prettytable import PrettyTable

import re

def c(s):
    return re.sub('\s+', ', ', s)

def show_table(rows, cols='', ncols=None):
    if ncols != None:
        cols = [('c%d' % i) for i in range(1, ncols+1)]
    else:
        cols = cols.split()
    table = PrettyTable( cols )
    table.add_rows(rows)
    print(table)


SHOW_CMD = True

def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

conn = psycopg2.connect(database='discord', user='isdb')
conn.autocommit = True
cur = conn.cursor()


us5='''
* US5
    As a: Community member
  I want: join servers
 So that: I can find community who share common interests
'''

print(us5)

def joinServer(server_id, user_id):
    tmplAdd = f''' 
        INSERT INTO In_server (server_id, user_id, date_joined, can_chat, can_voice)
            VALUES(%s, %s, CURRENT_TIMESTAMP, False, False)
'''
    cmd = cur.mogrify(tmplAdd, (server_id, user_id,))
    print_cmd(cmd)
    cur.execute(cmd)

def showInServer():
    cols = "Server_id, User_id, Date_joined, Can_chat, Can_voice"
    tmplShow = f'''
        SELECT * FROM In_server
    '''
    cmd = cur.mogrify(tmplShow, ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 

joinServer(1, 0) 
showInServer()
print("jonathan joins duck server")
print("each join server command can be run once since a user cannot join a server multiple times")




    

