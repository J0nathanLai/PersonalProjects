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


us10='''
* US10
    As a: Administrator
  I want: to rank users by interaction
 So that: I can analyze how active the members are
'''

print(us10)

def rankInteractions(server_id):
    cols = "rank userId username interactions"
    tmpl = f''' 
        WITH temp AS (
            SELECT u.user_id AS uid, u.username AS username, COUNT(m.message_id) AS count
              FROM servers AS s
              JOIN chat_channels AS c ON s.server_id = c.server_id
              JOIN channel_messages AS cm ON c.chat_channel_id = cm.chat_channel_id
              JOIN messages AS m ON cm.message_id = m.message_id
              JOIN users AS u ON m.sender_id = u.user_id
             WHERE s.server_id = %s
          GROUP BY u.user_id, u.username
        )
        SELECT (RANK() OVER w) AS rank, uid, username, count
          FROM temp
        WINDOW w AS (ORDER BY count DESC)
      ORDER BY rank
'''

    cmd = cur.mogrify(tmpl, (server_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 


print(rankInteractions(2))
print("given a server id, prints the users along with the amount of messages they have sent in the server, along with a rank, determined by amount of messages sent in server. results are sorted in ascending order of rank.")


