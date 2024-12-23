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


us2='''
* US2
    As a: Community Member
  I want: to join a voice channel
 So that: I can communicate with others in the same community
'''

print(us2)

def canVoice(user_id, voice_channel_id):
    tmpl = f'''
        SELECT EXISTS(
            SELECT 1 
              FROM In_server AS i JOIN Servers AS s On i.server_id = s.server_id
                   JOIN Voice_channels AS v ON v.server_id = s.server_id
             WHERE i.user_id = %s AND
                   v.voice_channel_id = %s AND 
                   i.can_voice = True
        )
    '''
    cur.execute(tmpl, (user_id, voice_channel_id))
    voiceAllowed = cur.fetchone()[0]
    return voiceAllowed

def joinVC(user_id, voice_channel_id, voiceAllowed):
    tmplDel = f''' 
        DELETE FROM In_voice_channel
         WHERE %s = user_id
    '''
    cmdDel = cur.mogrify(tmplDel, (user_id,))
    print_cmd(cmdDel)
    cur.execute(cmdDel)
    if voiceAllowed:
        tmplAdd = f'''
            INSERT INTO In_voice_channel (user_id, voice_channel_id)
                VALUES(%s, %s)
        '''
        cmdAdd = cur.mogrify(tmplAdd, (user_id, voice_channel_id,))
        print_cmd(cmdAdd)
        cur.execute(cmdAdd)
        print("user joined voice channel")
    else:
        print("user not allowed to join voice channel")

def showNewVC():
    cols = "user_id, vc_id"
    tmplShow = f'''
        SELECT * FROM In_voice_channel
    '''
    cmd = cur.mogrify(tmplShow, ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table(rows, cols) 

voiceAllowed1 = canVoice(0, 0)
joinVC(0, 0, voiceAllowed1)
voiceAllowed2 = canVoice(1, 2)
joinVC(1, 2, voiceAllowed2)
showNewVC()
print("user 0 Jonathan is allowed to join voice channel 0 and succesffully joins it")
print("user 1 Alicia is not allowed to join voice channel 2 and fails")







