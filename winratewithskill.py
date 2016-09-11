import sqlite3
from sklearn import tree
import random
import numpy as np
import matplotlib.pyplot as plt

# Just FYI this is all super hackathon code, a lot of copy/paste, very little thought put into efficiency, very little good commenting
# I just wanted the numbers as fast as possible so some of these were not coded to be elegant

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

players = []
opponents = []
heroes = []
profiles = []
c.execute('SELECT players.name, players.character, skill.skill FROM players JOIN skill ON players.name=skill.player ORDER BY skill')
for row in c: 
	players.append(row)
	opponents.append(row)
c.execute('SELECT DISTINCT character FROM players')
for row in c: heroes.append([row, 0, 0])

class Player:
	def __init__(self, givenname, char, tier):
		self.name = givenname
		self.skill = tier
		self.character = char
		self.playerrecord = []
		self.charrecord = []
		self.skillrecord = []
class Hero:
	def __init__(self, givenname):
		self.name = givenname
		self.players = []
		self.playerrecord = []
		self.charrecord = []
		self.skillrecord = []

def calculateskillforCharactersOverall():
	v = []
	for each in heroes:
		champion = Hero(each[0][0])
		c.execute('SELECT players.name, players.character, skill.skill FROM players JOIN skill ON players.name=skill.player WHERE character=?', (champion.name,))
		for row in c: champion.players.append(row)
		v.append(champion)

	for x in v:
		wins = 0
		losses = 0
		matches = 0
		games = []
		charplayers = []
		skillvector = []
		
		c.execute('SELECT name FROM players WHERE character=?', (x.name,))
		for row in c: charplayers.append(row[0])

		c.execute('SELECT matches.winner, s1.skill, matches.loser, s2.skill FROM matches JOIN skill s1 JOIN skill s2 JOIN players p1 JOIN players p2 ON s1.player=matches.winner AND s2.player=matches.loser AND p1.name=matches.winner AND p2.name=matches.loser WHERE p1.character=? OR p2.character=?', (x.name, x.name))
		for row in c: games.append(row)

		for game in games:
			skilldiffexists = 0
			if(game[0] in charplayers):
				wins += 1
				skilldiff = game[1] - game[3]
				for row in skillvector:
					if row[0] == skilldiff:
						skilldiffexists = 1
						row[1] += 1
						row[3] = float(row[1]) / (row[1] + row[2])
				if skilldiffexists == 0:
					skillvector.append([skilldiff, 1, 0, 1])
			if(game[2] in charplayers): #not elif, because both winner and loser can belong to charplayers (dittos)
				losses += 1
				skilldiff = game[3] - game[1]
				for row in skillvector:
					if row[0] == skilldiff:
						skilldiffexists = 1
						row[2] += 1
						row[3] = float(row[1]) / (row[1] + row[2])
				if skilldiffexists == 0:
					skillvector.append([skilldiff, 0, 1, 0])

		print x.name
		graphx = []
		graphy = []
		for row in skillvector:
			graphx.append(row[0])
			graphy.append(row[3])

		graphx = np.array(graphx)
		graphy = np.array(graphy)

		#chart
		plt.scatter(graphx, graphy)
		axes = plt.gca()
		axes.set_xlim([-7, 7])
		axes.set_ylim([0, 1])
		if(x.name == "Kirby"): continue #not letting me do kirby which is fine kirby's chart's obviously useless anyways
		fitline = np.poly1d(np.polyfit(graphx, graphy, 3))
		print fitline
		xp = np.linspace(-7, 7, 100)
		plt.plot(xp, fitline(xp), '-')
		plt.xlabel('Skill Difference')
		plt.ylabel('Winrate')
		title = x.name + " vs. all"
		plt.title(title)
		plt.show()



#for each in characters:
#This one in particular is really not optimized for speed so I'll probably rewrite it eventually
def calculateskillforCharactersvsCharacters():
	v = []
	for each in heroes:
		champion = Hero(each[0][0])
		c.execute('SELECT players.name, players.character, skill.skill FROM players JOIN skill ON players.name=skill.player WHERE character=?', (champion.name,))
		for row in c: champion.players.append(row)
		v.append(champion)

	skillchart = []
	difficulties = []
	lowrates = []
	char1 = raw_input("Character 1:")
	char2 = raw_input("Character 2:")

	for x in v:
		for a in v:
			skillrec = []
			for y in x.players:
				for b in a.players:
					wins = 0
					losses = 0
					matches = 0
					skilldiff = 0
					if b == y:
						continue
					if len(b) < 3:
						skilldiff = y[2] - 8
					elif len(y) < 3:
						skilldiff = 8 - b[2]
					else:
						skilldiff = y[2] - b[2]
					c.execute('SELECT * FROM matches WHERE winner = ? AND loser = ?', (y[0], b[0]))
					for row in c:
						wins += 1
						matches += 1
					c.execute('SELECT * FROM matches WHERE loser = ? AND winner = ?', (y[0], b[0]))
					for row in c:
						losses += 1
						matches += 1

					skillchartexists = 0
					for p in skillchart:
						if p[3] == skilldiff:
							p[0] += wins
							p[1] += losses
							if p[1] > 0:
								p[2] = float(p[0]) / (p[0]+p[1])
							else:
								p[2] = 1
							skillchartexists = 1

					if skillchartexists == 0:
						if losses > 0:
							skillchart.append([wins, losses, float(wins)/(wins+losses), skilldiff])
						else:
							skillchart.append([wins, losses, 1, skilldiff])

					skilldiffexists = 0
					thischar = b[1]
					for row in skillrec:
						if thischar == row[0]:
							if skilldiff == row[5]:
								skilldiffexists = 1
								row[1] += matches
								row[2] += wins
								row[3] += losses
								row[4] =  float(row[2]) / row[1]
					if skilldiffexists == 0:
						if losses > 0:
							skillrec.append([thischar, matches, wins, losses, float(wins)/matches, skilldiff])
						elif losses == 0 and wins > 1:
							skillrec.append([thischar, matches, wins, losses, 1, skilldiff])
			if x.name==char1:
				for row in skillrec:
					if row[0] == char2: 
						lowrates.append(row[4])
						difficulties.append(row[5])

	difficulties = np.array(difficulties)
	lowrates = np.array(lowrates)


	#chart
	plt.scatter(difficulties, lowrates)
	axes = plt.gca()
	axes.set_xlim([-7, 7])
	axes.set_ylim([0, 1])
	fitline = np.poly1d(np.polyfit(difficulties, lowrates, 3))
	xp = np.linspace(-7, 7, 100)
	plt.plot(xp, fitline(xp), '-')
	plt.xlabel('Skill Difference')
	plt.ylabel('Winrate')
	title = char1 + " vs. " + char2
	plt.title(title)
	plt.show()

#for each in players:
def calculateskillforPlayers():
	for each in players:
		y = Player(each[0], each[1], each[2])
		allwins = 0
		alllose = 0
		for every in opponents:
			x = Player(every[0], every[1], every[2])
			if y.name == x.name:
				continue
			oppchar = x.character
			skilldiff = y.skill - x.skill
			wins = 0
			losses = 0
			c.execute('SELECT * FROM matches WHERE winner=? AND loser=?', (y.name, x.name,))
			for row in c:
				wins += 1
				allwins += 1
			c.execute('SELECT * FROM matches WHERE winner=? AND loser=?', (x.name, y.name,))
			for row in c:
				losses += 1
				alllose += 1
			matches = wins + losses
			if matches == 0:
				continue
			winrate = (float(wins) / matches) * 100
			y.playerrecord.append([x.name, matches, winrate, skilldiff])

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
			
			skillexists = 0
			for z in y.skillrecord:
				if z[0] == oppchar:
					if z[4] == skilldiff:
						z[1] += matches
						z[2] += wins
						z[3] += losses
						skillexists = 1
						break
			if skillexists == 0:
				y.skillrecord.append([oppchar, matches, wins, losses, skilldiff])
		profiles.append(y)

	selectplayer = raw_input("Select Player:")
	for each in profiles:
		if each.name == selectplayer:
			print each.name
			print "%-*s" % (18, "Opposing Character"), "%-*s" % (7, "matches"), "%-*s" % (2, "W"), "%-*s" % (2, "L"), "%-*s" % (4, "diff")
			for row in each.skillrecord:
				print "%-*s" % (18, row[0]), "%-*s" % (7, row[1]), "%-*s" % (2, row[2]), "%-*s" % (2, row[3]), "%-*s" % (4, row[4])

def calculateskillforall():
	matches = []
	skillrecord = []
	for x in range(0, 15):
		skillrecord.append([0, 0, 0, 0, (x-7)])

	c.execute('SELECT matches.winner, s1.skill, matches.loser, s2.skill FROM matches JOIN skill s1 JOIN skill s2 ON s1.player=matches.winner AND s2.player=matches.loser ORDER BY s1.skill')
	for row in c: matches.append(row)
	for row in matches:
		skilldiffwinner = row[1] - row[3]
		skilldiffloser = row[3] - row[1]
		
		#wins at skilldiff
		skillrecord[skilldiffwinner+7][0] += 1
		skillrecord[skilldiffwinner+7][1] += 1
		skillrecord[skilldiffwinner+7][3] = float(skillrecord[skilldiffwinner+7][1]) /(skillrecord[skilldiffwinner+7][0])

		#losses at skilldiff
		skillrecord[skilldiffloser+7][0] += 1
		skillrecord[skilldiffloser+7][2] += 1
		skillrecord[skilldiffloser+7][3] = float(skillrecord[skilldiffloser+7][1]) /(skillrecord[skilldiffloser+7][0])

	graphx = []
	for row in skillrecord:
		graphx.append(row[4])
	graphy = []
	for row in skillrecord:
		graphy.append(row[3])

	graphx = np.array(graphx)
	graphy = np.array(graphy)

	print graphx
	print graphy

	#chart
	plt.scatter(graphx, graphy)
	axes = plt.gca()
	axes.set_xlim([-7, 7])
	axes.set_ylim([0, 1])
	fitline = np.poly1d(np.polyfit(graphx, graphy, 4))
	xp = np.linspace(-7, 7, 100)
	plt.plot(xp, fitline(xp), '-')
	plt.xlabel('Skill Difference')
	plt.ylabel('Winrate')
	title = "Melee Winrates by Relative Skill Level"
	plt.title(title)
	plt.show()

def generateTrainingSet():
	matches = []
	features = []
	labels = []
	c.execute('SELECT matches.winner, p1.character, s1.skill, matches.loser, p2.character, s2.skill FROM matches JOIN players p1 JOIN players p2 JOIN skill s1 JOIN skill s2 ON matches.winner=p1.name AND matches.loser=p2.name AND p1.name=s1.player AND p2.name=s2.player ORDER BY s1.skill-s2.skill')
	for row in c: matches.append(row)

	for row in players:
		x = Player(row[0], row[1], row[2])
		profiles.append(x)

	#print "%-*s" % (18, "Player 1"), "%-*s" % (2, "S1"), "%-*s" % (18, "Player 2"), "%-*s" % (2, "S2"), "%-*s" % (15, "P1 Char"), "%-*s" % (15, "P2 Char"), "%-*s" % (15, "Winner"), "Record"
	
	for row in matches:
		#Select both players' profiles
		for x in profiles:
			if x.name == row[0]: Winner = x
		for y in profiles:
			if y.name == row[3]: Loser = y

		#if they don't have a match record, create one and put 0-0 in it
		wrecordexists = 0
		lrecordexists = 0
		wrecord = []
		lrecord = []
		for z in Winner.playerrecord:
			if z[0] == Loser.name: 
				wrecord = z[1]
				wrecordexists = 1
				break;
		if wrecordexists == 0:
			Winner.playerrecord.append([Loser.name, [0,0]])
			Loser.playerrecord.append([Winner.name, [0,0]])
			wrecord = [0,0]
		for z in Loser.playerrecord:
			if z[0] == Winner.name: 
				lrecord = z[1]
				lrecordexists = 1
				break;
		if lrecordexists == 0:
			Winner.playerrecord.append([Loser.name, [0,0]])
			Loser.playerrecord.append([Winner.name, [0,0]])
			lrecord = [0,0]

		#randomly select which order to place into the set, so that player 1 doesn't always win
		order = random.getrandbits(1)
		winrate = -1

		if order == 1:
			if(wrecord[1] == 0):
				if (wrecord[0] != 0):
					winrate = 1
				else:
					winrate = 0
			else:
				winrate = float(wrecord[0]/(wrecord[0]+wrecord[1]))
			features.append([row[2]-row[5], chartonum(row[1]), chartonum(row[4]), winrate])
			labels.append(1)
			#print "%-*s" % (18, row[0]), "%-*s" % (2, row[2]), "%-*s" % (18, row[3]), "%-*s" % (2, row[5]), "%-*s" % (15, row[1]), "%-*s" % (15, row[4]), "%-*s" % (15, wrecord), row[0]
		if order == 0:
			if(lrecord[1] == 0):
				if (lrecord[0] != 0):
					winrate = 1
				else:
					winrate = 0
			else:
				winrate = float(lrecord[0]/(lrecord[0]+lrecord[1]))
			features.append([row[5]-row[2], chartonum(row[4]), chartonum(row[1]), winrate])
			labels.append(0)
			#print "%-*s" % (18, row[3]), "%-*s" % (2, row[5]), "%-*s" % (18, row[0]), "%-*s" % (2, row[2]), "%-*s" % (15, row[4]), "%-*s" % (15, row[1]), "%-*s" % (15, lrecord), row[0]

		#incremement winners wins by 1
		for z in Winner.playerrecord:
			if z[0] == Loser.name:
				z[1][0] += 1
				break
		#increment losers losses by 1
		for z in Loser.playerrecord:
			if z[0] == Winner.name:
				z[1][1] += 1
				break

	features = np.array(features)
	labels = np.array(labels)

	clf=tree.DecisionTreeClassifier()
	clf=clf.fit(features, labels)
	
	#import pydotplus
	#from StringIO import StringIO
	#dot_data = StringIO()
	#tree.export_graphviz(clf, out_file=dot_data, feature_names=["skill difference", "character p1", "character p2", "winrate"], class_names=["win", "loss"] )
	#graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
	#graph.write_pdf("melee.pdf")

	guess(clf)

#random order so classifier doesn't think low/high number necessarily means "better character"
def chartonum(char):
	if char == "Fox": return 4
	if char == "Falco": return 3
	if char == "Sheik": return 6
	if char == "Jigglypuff": return 1
	if char == "Marth": return 0
	if char == "Peach": return 2
	if char == "Falcon": return 7
	if char == "Ice Climbers": return 5
	return 8

def guess(clf):
	p1 = raw_input("Player 1:")
	found = 0
	for x in profiles:
		if x.name == p1: 
			player1 = x
			found = 1
	if found == 0:
		flow = raw_input("Player not found: add? [y/n]:")
		if flow == "y":
			newchar = raw_input("Char? ")
			newskill = int(raw_input("Skill? "))
			c.execute('INSERT INTO players VALUES (?, ?)', (p1, newchar))
			c.execute('INSERT INTO skill VALUES (?, ?)', (p1, newskill))
			player1 = Player(p1, newchar, newskill)
			profiles.append(player1)
			guess(clf)
		if flow == "n":
			guess(clf)


	p2 = raw_input("Player 2:")
	found = 0
	for x in profiles:
		if x.name == p2: 
			player2 = x
			found = 1
	if found == 0:
		flow = raw_input("Player not found: add? [y/n]:")
		if flow == "y":
			newchar = raw_input("Char? ")
			newskill = int(raw_input("Skill? "))
			c.execute('INSERT INTO players VALUES (?, ?)', (p2, newchar))
			c.execute('INSERT INTO skill VALUES (?, ?)', (p2, newskill))
			player2 = Player(p2, newchar, newskill)
			profiles.append(player2)
			guess(clf)
		if flow == "n":
			guess(clf)

	recordexists = 0
	winloss = []
	for record in player1.playerrecord:
		if record[0] == p2:
			winloss = record
			if(winloss[1][1] == 0):
				if (winloss[1][0] != 0):
					winrate = 1
				else:
					winrate = 0
			else:
				winrate = float(winloss[1][0]/(winloss[1][0]+winloss[1][1]))
			recordexists = 1
			break
	if recordexists == 0:
		winrate = -1

	vector = [player1.skill-player2.skill, chartonum(player1.character), chartonum(player2.character), winrate]
	vector = np.array(vector).reshape(1, -1)

	prediction = clf.predict(vector)	
	if prediction == 0:
		print player2.name
	if prediction == 1:
		print player1.name
	guess(clf)

def main():
	cmd = raw_input("select command: ")
	if cmd == "-co":
		calculateskillforCharactersOverall()
	elif cmd == "-p":
		calculateskillforPlayers()
	elif cmd == "-cvc":
		calculateskillforCharactersvsCharacters()
	elif cmd == "-a":
		calculateskillforall()
	elif cmd == "-t":
		generateTrainingSet()
	else:
		main()

main()