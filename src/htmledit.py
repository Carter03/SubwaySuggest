from bs4 import BeautifulSoup as bs

class Editor():
    def __init__(self, htmlpath, subpath):
        self.indexPath = htmlpath
        self.subpath = subpath
        self.soup = bs(open(indexPath), 'html.parser')
    
    def ReplaceSubs(data): # list[4] of [sub num, sub desc, sub cost]
        subdata = data.copy()
        for idx, sub in enumerate(subdata):
            subImg = soup.find(attrs={'id':f'sub{idx+1}'})
            sub['src'] = r'../static/images/sub1.jpeg'


        

indexPath = 'utils/templates/index.html'

soup = bs(open(indexPath), 'html.parser')

for i in range(4):
    sub = soup.find(attrs={'id':f'sub{i+1}'})
    sub['src'] = r'../static/images/sub1.jpeg'

placeCardClasses = soup.find_all('img', class_='place-card-image')

with open(indexPath, 'w') as html:
    html.write(str(soup))