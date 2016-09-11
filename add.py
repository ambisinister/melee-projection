import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

URL = input("enter URL: ")

res = (requests.get("\"" + URL + "\""))
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text)
event = soup.head.title.text.partition('/')[0]
event = event.partition('-')[0]
print event

games = soup.find_all('div', class_="bracket-game")

for game in range (0, len(games)):
	round = games[game].div['class'][0]
	round = '.' + round
	cells = games[game].select(round)
	if(len(cells) > 1):
		player1 = cells[0].span.getText()
		player2 = cells[1].span.getText()
		player1 = player1.strip()
		player2 = player2.strip()

		if('style' in cells[0].attrs):
			if(cells[0]['style'] == 'font-weight:bold'):
				print player1 + " over " + player2
				c.execute('INSERT INTO matches VALUES (?, ?, ?);', (player1, player2, event))
		if('style' in cells[1].attrs):
			if(cells[1]['style'] == 'font-weight:bold'):
				print player2 + " over " + player1
				c.execute('INSERT INTO matches VALUES (?, ?, ?);', (player2, player1, event))

conn.commit()
conn.close()