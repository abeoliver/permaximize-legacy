# server.py
# Game
# Plexivate Software

import MySQLdb as sql
from tournament import Player

def getUserList(table):
    print 1
    try:
        con = sql.connect('63.142.111.132', 'GameUser', 'ROBO036T', 'Game')
        print 2
        cur = con.cursor(sql.cursors.DictCursor)
        print 3
        cur.execute("SELECT * FROM BCVGC-5-28-16;")
        print 4
        rows = cur.fetchall()
        print 5
    except sql.Error, e:
        print 6
        print "ERROR :: %d, %s" % (e.args[0], e.args[1])
    players = []
    for row in rows:
        name = row["first"] + " " + row["last"]
        records = [row["wins"], row["losses"]]
        p = Player(name, row["passcode"], records, row["lastLevel"])
        players.append(p)
    con.close()
    return players