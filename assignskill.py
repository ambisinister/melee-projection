import sqlite3
conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

#c.execute('DROP TABLE IF EXISTS skill')
#c.execute('CREATE TABLE skill (player TEXT, skill INT)')

players = []
data = []
c.execute('SELECT player FROM skill')
for row in c: data.append(row[0])
c.execute('SELECT DISTINCT loser FROM matches')
for row in c: players.append(row[0])

for row in players:
	if row not in data:
		skill = input("assign skill for " + row + " : ")
		c.execute('INSERT INTO skill VALUES (?, ?);', (row, skill))

conn.commit()
conn.close()

print "completed"