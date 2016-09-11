import requests, bs4
import sqlite3

conn = sqlite3.connect('matches.sqlite3')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS matches ')
c.execute('CREATE TABLE matches (winner TEXT, loser TEXT, event TEXT)')

res = []

res.append(requests.get("http://wiki.teamliquid.net/smash/EVO_2016/Melee/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Get_On_My_Level_2016/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/GENESIS_3/Melee/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/The_Big_House_5/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/EVO_2015/Melee/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/CEO_2015/Top_32"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Apex_2015/Melee/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/WTFox_2/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/CEO_2016/Melee/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Smash_%27N%27_Splash_2/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/DreamHack_Austin_2016/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Enthusiast_Gaming_Live_Expo/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Smash_Summit_2/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Pound_2016/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/PAX_Arena/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Battle_of_the_Five_Gods/Finals_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/DreamHack_Winter_2015/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Smash_Summit/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/HTC_Throwdown/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Paragon_Los_Angeles_2015/Singles"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Super_Smash_Con/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/WTFox/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/FC_Smash_15XR:_Return/Singles"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Press_Start/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Sandstorm/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/I%27m_Not_Yelling!/Singles_Bracket"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Paragon_2015/Singles_Top_64_Winners"))
res.append(requests.get("http://wiki.teamliquid.net/smash/Paragon_2015/Singles_Top_64_Losers"))

for page in range (0, len(res)):
	res[page].raise_for_status()
	soup = bs4.BeautifulSoup(res[page].text)

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