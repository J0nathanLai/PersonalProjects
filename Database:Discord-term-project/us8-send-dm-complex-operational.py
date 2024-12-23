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


us8='''
* US8
    As a: Community member
  I want: to send a direct message
 So that: I can communicate with peers in different time zones
'''

print(us8)

def nextDMid():
    tmpl = f'''
        SELECT MAX(Message_id)
          FROM Messages
'''
    cur.execute(tmpl)
    nextID = cur.fetchone()[0] + 1
    return nextID

def sendDM(message_id, message, sender_id, receiver_id):
    tmpl = f''' 
        INSERT INTO Messages(Message_id, Message, Time_sent, Sender_id)
            VALUES(%s, %s, CURRENT_TIMESTAMP, %s);
        INSERT INTO Dm_messages(Message_id, Receiver_id)
            VALUES(%s, %s);
'''
    cmd = cur.mogrify(tmpl, (message_id, message, sender_id, message_id, receiver_id))
    print_cmd(cmd)
    cur.execute(cmd)

def showDM(sender_id, receiver_id):
    cols = "sender_id, receiver_id, message"
    tmpl = f''' 
        SELECT m.Sender_id, d.Receiver_id, m.message
          FROM Messages AS m JOIN Dm_messages AS d ON m.Message_id = d.Message_id
         WHERE m.Sender_id = %s 
               AND d.Receiver_id = %s
         ORDER BY m.message_id DESC
'''
    cmd = cur.mogrify(tmpl, (sender_id, receiver_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 

nextDM1 = nextDMid()
sendDM(nextDM1, "hello Alicia", 0, 1)
showDM(0, 1)
nextDM2 = nextDMid()
sendDM(nextDM2, "Xiaoying, do you know I actually really love database", 2, 3)
showDM(2, 3)
print("Jonathan user0 sends DM to Alicia user1 saying 'hello Alicia'")
print("Raja user2 sends DM to Xiaoying user3 saying 'Xiaoying, do you know I actually really love database'")



