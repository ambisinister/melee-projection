import sqlite3
import numpy as np
import matplotlib.pyplot as plt

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

#character usage by match
c.execute('SELECT DISTINCT character FROM players')
chars = []
games = []
values = []
colors = ["Red", "Pink", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet", "White", "Cyan", "Black", "Black", "Black", "Black", "Black", "Black", "Black", "Black"]

for row in c: chars.append([row[0], 0])

c.execute('SELECT * FROM matches')
for row in c: games.append(row)
for row in games:
	for a in row:
		c.execute('SELECT character FROM players WHERE name = ?', (a,))
		for row in c: thischar = row[0]
		for x in chars:
			if x[0] == thischar:
				x[1] += 1
total = 0
for x in chars:
	total += x[1]
for x in chars:
	if(total != 0):
		values.append((float(x[1]) / total) * 100)

labels = []
for row in chars: labels.append(row[0])

plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, pctdistance=1.15, labeldistance=1.3, radius=0.5)
plt.axis('equal')
plt.show()