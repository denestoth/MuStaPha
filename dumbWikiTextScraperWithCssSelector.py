import requests
from bs4 import BeautifulSoup
from lxml import html 

path = 'table.wikitable>tbody>tr>th>a'
r = requests.get('https://en.wikipedia.org/wiki/List_of_Indian_Nobel_laureates')
soup = BeautifulSoup(r.text, 'lxml')
names = soup.select(path)
for name in names:
	print(name.text)
