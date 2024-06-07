from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

connection = sqlite3.connect("google_bot.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS visit(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               collected_on TEXT NOT NULL,
               URL TEXT NOT NULL
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS visit_items(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               visit_id INTEGER NOT NULL,
               name TEXT NOT NULL,
               rank INTEGER NOT NULL,
               FOREIGN KEY (visit_id) REFERENCES visit (id)
)""")

url = "https://steam250.com/most_played"
collected_on = datetime.datetime.now().strftime("%d-%m-%Y %X")
cursor.execute("INSERT INTO visit (collected_on, URL) VALUES (?, ?)", (collected_on, url))
connection.commit()

visit_id = cursor.lastrowid 

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

game_titles = soup.find_all('span', class_='title')

count = 1
for title in game_titles:
    if count >= 251:
        break
    game_title_text = title.text.split('. ', 1)[-1]
    print(f'{game_title_text} staat op rank {count}')
    cursor.execute("INSERT INTO visit_items (visit_id, name, rank) VALUES (?, ?, ?)", (visit_id, game_title_text, count))
    count += 1

connection.commit()
connection.close()
