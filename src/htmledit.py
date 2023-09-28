from bs4 import BeautifulSoup as bs

indexPath = 'utils/templates/index.html'

soup = bs(open(indexPath), 'html.parser')
subs = soup.find_all("img", class_ = "sub")

for sub in subs:
    sub['src'] = ''

with open(indexPath, 'w') as html:
    html.write(str(soup))