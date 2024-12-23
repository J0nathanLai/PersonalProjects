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


us1='''
* US1
    As a: Community Member
  I want: search for servers
 So that: I can find communities who share common interests
'''

print(us1)

def showServers():
    cols = "servers"
    tmpl = f''' 
        SELECT server_name FROM servers
'''

    cmd = cur.mogrify(tmpl, ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 

showServers()
print("lists out all the servers")



