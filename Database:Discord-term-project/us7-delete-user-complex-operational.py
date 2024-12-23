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


us7='''
* US7
    As a: User
  I want: to delete my account
 So that: I can stop using discord
'''

print(us7)
#delete function: deletes user from community_member, content_creator, or admin table, sets all the fields in user to empty values
def deleteUser(user_id):
    cols = "uid"
    tmpl = f''' 
    DELETE from community_members WHERE user_id = %s;
    DELETE from administrators WHERE user_id = %s;
    DELETE from content_creators WHERE user_id = %s;
    UPDATE users
        SET username = '!', status = 'deleted', status_message = '!', email = '!', age = 0, pronouns = '!'
        WHERE user_id = %s;
'''
    cmd = cur.mogrify(tmpl, (user_id, user_id, user_id, user_id))
    # print_cmd(cmd)
    cur.execute(cmd)

def showDeletedUser():
    cols = "uid username status status_message email age pronouns"
    tmpl = f''' 
    SELECT * FROM users;
'''
    cur.execute(tmpl)
    rows = cur.fetchall()
    # pp(rows)
    show_table(rows, cols) 

def showDeletedUserServer(deleted_user_id):
    cols = "sid uid joined canchat canvoice"
    tmpl = f''' 
        SELECT * FROM in_server WHERE user_id = %s
    '''
    cmd = cur.mogrify(tmpl, (deleted_user_id,))
    cur.execute(cmd)
    rows = cur.fetchall()
    # pp(rows)
    show_table(rows, cols)

def showDeletedUserVoice(deleted_user_id):
    cols = "cid uid"
    tmpl = f''' 
        SELECT * FROM in_voice_channel WHERE user_id = %s
    '''
    cmd = cur.mogrify(tmpl, (deleted_user_id,))
    cur.execute(cmd)
    rows = cur.fetchall()
    # pp(rows)
    show_table(rows, cols)

print(deleteUser(6))
showDeletedUser()  #shows user table without deleted user's info
showDeletedUserServer(6)  #shows In_server table without the deleted user
showDeletedUserVoice(6)  #shows In_voice_channel table without the deleted user

print("deletes specified user from corresponding child of user (content creator, community member, or administrator), then sets all the values in user to default values. When user is deleted from one of the three tables, the trigger runs to delete all instances of the user from voice channels and servers. (triggers are created in initialize.sql)")


