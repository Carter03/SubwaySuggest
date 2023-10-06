from difflib import get_close_matches
import pandas as pd
from datetime import datetime

class Logger:
    def __init__(self, prefsPath, dataPath, ageGroups):
        self.prefsPath = prefsPath
        self.dataPath = dataPath
        self.ageGroups = [(int(group.split()[0]), int(group.split()[-1])) for group in ageGroups]
        self.prefsDf = pd.read_excel(prefsPath)
        self.dataDf = pd.read_excel(dataPath)

    def ContinuouslyLog(self):
        while True:
            self.GetResponses()
    
    def GetResponses(self):
        subInput = input('What did the customer purchase?  ')
        subNames = list(self.dataDf.loc[:, 'Name'])

        subName = ''
        if closestSub := get_close_matches(subInput, subNames):
            subName = closestSub[0]
            print(subName, end='\n\n')
        elif subInput.startswith(r'#'):
            subName = [sub for sub in subNames if f'{subInput.split()[0]} ' in sub][0]
            print(subName, end='\n\n')
        elif subInput[0].isnumeric():
            subName = [sub for sub in subNames if f'#{subInput.split()[0]} ' in sub][0]
            print(subName, end='\n\n')
        else:
            print('Sub not found...')
            return
        
        ageInput = int(input('What was the customer\'s age?  '))

        closestAge = 1000
        closestGroup = None
        for lower, upper in self.ageGroups:
            if abs(ageInput - lower) < closestAge:
                closestAge = abs(ageInput - lower)
                closestGroup = (lower, upper)
            if abs(ageInput - upper) < closestAge:
                closestAge = abs(ageInput - upper)
                closestGroup = (lower, upper)
        print(closestGroup, end='\n\n')

        genderInput = input('What was the customer\'s gender? ')

        closestGender = ''
        if 'f' in genderInput.lower() or genderInput.lower() == 'girl':
            closestGender = 'Female'
        else:
            closestGender = 'Male'
        print(closestGender)

        self.UpdatePrefs(subName, closestGroup, closestGender)

    def UpdatePrefs(self, subName, ageGroup, closestGender):
        group = f'{ageGroup[0]} - {ageGroup[1]}'
        newRow = pd.DataFrame(
                            {
                                'Time': str(datetime.now().strftime('%m/%d/%Y %H:%M:%S')), 
                                'Age': str(group),
                                'Gender': closestGender,
                                'Subs': f'{subName};'
                            }, index=[-1])
        
        print(newRow, end='\n\n')

        
        df_excel = pd.read_excel(self.prefsPath, sheet_name='Sheet1')
        # appended = df_excel.append(newRow)
        appended = pd.concat([df_excel.iloc[:, 1:], newRow], axis=0)

        with pd.ExcelWriter(self.prefsPath, mode="a", if_sheet_exists='replace') as f:
            appended.to_excel(f, sheet_name='Sheet1')

if __name__ == '__main__':
    log = Logger(r'..\data\SandwichPrefsData.xlsx', r'..\data\Subdata.xlsx', ['0 - 2', '4 - 6', '8 - 12', '15 - 20', '25 - 32', '38 - 43', '48 - 53', '60 - 100'])
    log.ContinuouslyLog()