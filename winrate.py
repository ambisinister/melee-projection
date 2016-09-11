-import sqlite3
conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

players = []
opponents = []
heroes = []
c.execute('SELECT DISTINCT winner FROM matches')
for row in c: 
	players.append(row)
	opponents.append(row)
c.execute('SELECT DISTINCT loser FROM matches')
for row in c:
	if row not in players:
		players.append(row)
		opponents.append(row)
c.execute('SELECT DISTINCT character FROM players')
for row in c: heroes.append([row, 0, 0])

class Player:
	def __init__(self, givenname):
		self.name = givenname
		self.playerrecord = []
		self.charrecord = []
class Hero:
	def __init__(self, givenname):
		self.name = givenname
		self.players = []
		self.playerrecord = []
		self.charrecord = []


#for each in characters:
v = []
for each in heroes:
	champion = Hero(each[0][0])
	c.execute('SELECT name FROM players WHERE character=?', (champion.name,))
	for row in c: champion.players.append(row)
	v.append(champion)

for x in v:
	for a in v:
		wins = 0
		losses = 0
		matches = 0
		for y in x.players:
			for b in a.players:
				if b == y:
					continue
				c.execute('SELECT * FROM matches WHERE winner = ? AND loser = ?', (y[0], b[0]))
				for row in c:
					wins += 1
					matches += 1
				c.execute('SELECT * FROM matches WHERE loser = ? AND winner = ?', (y[0], b[0]))
				for row in c:
					losses += 1
					matches += 1

		if(matches > 0):
			print a.name, (float(wins)/matches)*100, "%"

#for each in players:
for each in players:
	y = Player(each[0])
	allwins = 0
	alllose = 0
	for x in opponents:
		if y.name == x:
			continue
		c.execute('SELECT character FROM players WHERE name=?', (x[0],))
		for row in c: oppchar = row
		wins = 0
		losses = 0
		c.execute('SELECT * FROM matches WHERE winner=? AND loser=?', (y.name, x[0],))
		for row in c:
			wins += 1
			allwins += 1
		c.execute('SELECT * FROM matches WHERE winner=? AND loser=?', (x[0], y.name,))
		for row in c:
			losses += 1
			alllose += 1
		matches = wins + losses
		if matches == 0:
			continue
		winrate = (float(wins) / matches) * 100
		y.playerrecord.append([x[0], matches, winrate])

		charexists = 0
		for z in y.charrecord:
			if z[0] == oppchar:
				z[1] += matches
				z[2] += wins
				z[3] += losses
				charexists = 1
				break
		if charexists == 0:
			y.charrecord.append([oppchar, matches, wins, losses])
		#y.charrecord.append([oppchar, matches, wins, losses, skilldiff])

	print y.name, float(allwins) / (allwins + alllose) * 100, "%"
