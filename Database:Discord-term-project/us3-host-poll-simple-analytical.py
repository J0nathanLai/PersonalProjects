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


us3='''
* US3
    As a: Content Creator
  I want: host polls using reactions
 So that: I can gauge interest in certain topics
'''

print(us3)

def hostPoll(message_id):
    cols = "emoji count"
    tmpl = f''' 
        SELECT reaction_emoji, COUNT(reaction_id)
          FROM reactions
         WHERE message_id = %s
      GROUP BY reaction_emoji
'''

    cmd = cur.mogrify(tmpl, (message_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 


hostPoll(0)
print("displays emojis that have been reacted and the amount of each emoji reacted on specified message. ")



