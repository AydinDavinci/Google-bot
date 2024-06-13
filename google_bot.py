from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

def main():
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

    cursor.execute("""CREATE TABLE IF NOT EXISTS visit_item_info(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   visit_item_id INTEGER NOT NULL,
                   key TEXT NOT NULL,
                   value TEXT NOT NULL,
                   FOREIGN KEY (visit_item_id) REFERENCES visit_items (id)
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
        if count >= 50:
            break
        game_title_text = title.text.split('. ', 1)[-1]
        cursor.execute("INSERT INTO visit_items (visit_id, name, rank) VALUES (?, ?, ?)", (visit_id, game_title_text, count))
        connection.commit()
        visit_item_id = cursor.lastrowid

        game_div = title.find_parent('div', class_='appline')
        rating = soup.find('span', class_= 'rating')
        players = soup.find('span', class_ = 'players')

        if game_div:
            date_out = game_div.find('span', class_ = 'date')

            if date_out:
                cursor.execute('INSERT INTO visit_item_info (visit_item_id, key, value) VALUES (?,?,?)', (visit_item_id, 'date_out', date_out.text.strip()))

        if players:
            cursor.execute('INSERT INTO visit_item_info (visit_item_id, key, value) VALUES (?,?,?)', (visit_item_id, 'players', players.text.strip()))

        if rating:
            cursor.execute('INSERT INTO visit_item_info (visit_item_id, key, value) VALUES (?,?,?)', (visit_item_id, 'rating', rating.text.strip()))
        
        count += 1
   
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()

