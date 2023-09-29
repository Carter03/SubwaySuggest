from bs4 import BeautifulSoup as bs

indexPath = 'utils/templates/index.html'

soup = bs(open(indexPath), 'html.parser')

for i in range(4):
    sub = soup.find(attrs={'id':f'sub{i+1}'})
    sub['src'] = r'../static/images/sub1.jpeg'

placeCardClasses = soup.find_all('img', class_='place-card-image')

with open(indexPath, 'w') as html:
    html.write(str(soup))