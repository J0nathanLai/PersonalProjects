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


us6='''
* US6
    As a: Server administrator
  I want: to assign server permissions
 So that: the server settings cannot be modified by untrusted individuals
'''

print(us6)

def isAdmin(admin_id):
    tmpl = f'''
        SELECT EXISTS(
            SELECT 1 
              FROM Administrators
             WHERE user_id = %s
        )
    '''
    cur.execute(tmpl, (admin_id, ))
    inAdminTable = cur.fetchone()[0]
    return inAdminTable

def updatePermissions(admin_id, server_id, user_id, can_chat, can_voice):
    if isAdmin(admin_id):
        tmplUpdate = f'''
        UPDATE In_server
           SET Can_chat = %s, Can_voice = %s
         WHERE Server_id = %s AND User_id = %s
        '''
        cmd = cur.mogrify(tmplUpdate, (can_chat, can_voice, server_id, user_id,))
        print_cmd(cmd)
        cur.execute(cmd)
    else:
        print("User is not admin")

def showPermissions():
    cols = "Server_id, User_id, Date_joined, Can_chat, Can_voice"
    tmplShow = f'''
        SELECT * 
          FROM In_server
    '''
    cmd = cur.mogrify(tmplShow, ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 

updatePermissions(2, 2, 1, True, True) 
showPermissions()
updatePermissions(5, 2, 0, True, True) 
showPermissions()

print("Raja gives Alicia permissions to chat and voice but fails because Raja is not an admin")
print("Carol gives Jonathan permissions to chat and voice as Carol is an administrator")


