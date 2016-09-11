import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

#c.execute('DROP TABLE IF EXISTS players')
#c.execute('CREATE TABLE players (name TEXT, character TEXT)')

tags = []
chars = []
rows = []

count = 0

c.execute('SELECT DISTINCT winner FROM matches')
for row in c:
	rows.append(row[0])


c.execute('SELECT name FROM players')
for row in c:
	tags.append(row[0])

for row in rows:
	name = row
	if name not in tags:
		if count == 0:
			count = 1
			continue;
		character = raw_input('CHARACTER FOR ' + name +':')
		c.execute('INSERT INTO players VALUES (?, ?);', (name, character))

conn.commit()
conn.close()