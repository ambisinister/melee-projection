import requests, bs4
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

chars = []
values = []
colors = ["Red", "Pink", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet", "White", "Black", "Black", "Black", "Black", "Black", "Black", "Black", "Black", "Black"]

c.execute('SELECT DISTINCT character FROM players')

for row in c:
	chars.append(row[0])

for characters in chars:
	count = 0
	c.execute('SELECT * FROM players WHERE character = \"' + characters + "\"")
	for row in c:
		count += 1
	values.append((float(count) / 340) * 100)

plt.pie(values, labels=chars, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, pctdistance=1.15, labeldistance=1.3, radius=0.5)
plt.axis('equal')
plt.show()