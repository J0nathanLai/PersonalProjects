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


us4='''
* US4
    As a: Content Creator
  I want: to count new users within a period
 So that: I can  see how well my brand is flourishing
'''

print(us4)

def countNewUsers(server_id, start, end):
    cols = "count"
    tmpl = f''' 
        SELECT COUNT(user_id)
          FROM in_server
         WHERE Server_id = %s
               AND Date_joined BETWEEN %s AND %s;
'''

    cmd = cur.mogrify(tmpl, (server_id, start, end))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 


countNewUsers(0, 'Sun Sep 29 2024 02:29:58', 'Sun Dec 15 2024 02:29:58')
print("displays the amount of new users in specified server within specified time frame.")


