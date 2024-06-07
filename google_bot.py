from bs4 import BeautifulSoup
import requests

url = "https://steam250.com/most_played"

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
    count += 1
