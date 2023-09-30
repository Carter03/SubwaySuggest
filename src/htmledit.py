from bs4 import BeautifulSoup as bs
import pandas as pd

class Editor():
    def __init__(self, htmlpath='utils/index.html', subpath='images/', excelpath=r'..\data\Subdata.xlsx'): # subpath = '../static/images/
        self.indexPath = htmlpath
        self.subpath = subpath
        self.soup = bs(open(self.indexPath), 'html.parser')
        self.subDataExcel = pd.read_excel(excelpath)
    
    def ReplaceSubs(self, data): # list[4] of [sub name, sub desc, sub cost]
        subdata = data.copy()

        for idx, sub in enumerate(subdata):
            subImg = self.soup.find(attrs={'id':f'sub{idx+1}'})
            subTitle = self.soup.find(attrs={'id':f'title{idx+1}'})
            subDesc = self.soup.find(attrs={'id':f'desc{idx+1}'})
            subCost = self.soup.find(attrs={'id':f'cost{idx+1}'})
            
            subImg['src'] = f'{self.subpath}{self.ConvertName(sub[0])}.jpeg'
            subTitle.string = sub[0]
            subDesc.string = sub[1]
            subCost.string = '$' + sub[2]

        self.UpdateHTML()
    
    def UpdateHTML(self):
        with open(self.indexPath, 'w') as html:
            html.write(str(self.soup))
    
    def ConvertName(self, name):
        return name[1:].replace(' ', '_')
    
    def DataFromName(self, subName):
        result = self.subDataExcel.isin([subName])
        seriesObj = result.any()
        try:
            col = seriesObj[seriesObj == True].index[0]
            row = result[col][result[col] == True].index[0]
            return [str(i) for i in list(self.subDataExcel.loc[row])]
        except:
            print("ERROR: " + subName + " WAS NOT FOUND IN Subdata.xlsx")
        return [None, None, None]

        


if __name__ == '__main__':
    editor = Editor(htmlpath='utils/templates/index.html', subpath='../static/images/')

    subData = editor.DataFromName('#1 The Philly')
    print(subData)
    editor.ReplaceSubs([subData])