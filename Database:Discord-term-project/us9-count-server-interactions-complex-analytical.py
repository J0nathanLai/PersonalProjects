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


us9='''
* US9
    As a: Community Member
  I want: to count my interactions with each server (messages, reactions, voice calls)
 So that: I can gauge my activity with each community
'''

print(us9)

def countInteractions(user_id):
    cols = "servername serverid messages interactions total"
    tmpl = f''' 
        WITH msgs AS (
            SELECT s.server_id AS sid, COUNT(c.chat_channel_id) AS cntm
            FROM servers AS s 
            LEFT JOIN chat_channels AS c ON s.server_id = c.server_id
            LEFT JOIN channel_messages AS cm ON c.chat_channel_id = cm.chat_channel_id
            LEFT JOIN messages AS m ON m.message_id = cm.message_id
            WHERE m.sender_id = %s
            GROUP BY s.server_id
        ),
        reactns AS (
            SELECT s.server_id AS sid, COUNT(r.reaction_id) AS cntr
            FROM servers AS s
            JOIN chat_channels AS c ON s.server_id = c.server_id
            JOIN channel_messages AS cm ON c.chat_channel_id = cm.chat_channel_id
            JOIN reactions AS r ON cm.message_id = r.message_id
            WHERE r.user_id = %s
            GROUP BY s.server_id
        )
        SELECT s.server_name, s.server_id, coalesce(cntm, 0), coalesce(cntr, 0), (coalesce(cntm, 0) + coalesce(cntr, 0))
        FROM servers AS s FULL OUTER JOIN msgs AS m ON s.server_id = m.sid 
        FULL OUTER JOIN reactns AS r ON s.server_id = r.sid
        
'''




    cmd = cur.mogrify(tmpl, (user_id, user_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 


countInteractions(2)
print("counts and categorizes the interactons made by user 2 Raja")