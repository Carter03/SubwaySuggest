import pandas as pd
import numpy as np

class DataManager():
    def __init__(self):
        self.gender_groups = ['Male', 'Female']
        self.age_groups = ['0 - 2', '4 - 6', '8 - 12', '15 - 20', '25 - 32', '38 - 43', '48 - 53', '60 - 100']

        self.dataPath = r'..\data\SandwichPrefsData.xlsx'

        self.df = pd.read_excel(self.dataPath)
        self.data = self.df.to_numpy().copy()[:, 6:]

        def GetSandMappings():
            factors = pd.factorize([i for list in [i.split(';') for i in self.data[:, 0]] for i in list if i])[1] # retrieve sandwich names from string, get unique IDs for them
            mappings = dict(zip(factors, range(len(factors))))

            return mappings

        self.sandMappings = GetSandMappings()                                                  # convert sandwich name to ID
        self.ageMappings = dict(zip(self.age_groups, range(len(self.age_groups))))             # convert age to ID
        self.genderMappings = dict(zip(self.gender_groups, range(len(self.gender_groups))))    # convert gender name to ID

        self.totalMappings = {**self.sandMappings, **self.ageMappings, **self.genderMappings}   # IDs are in separate sections of modelData, so mappings can be combined

    def ApplyMappings(self, x):
        if type(x) == list:
            return list(map(self.ApplyMappings, x))
        return self.totalMappings[x] if not ';' in x else [self.totalMappings[i] for i in x.split(';') if i]
    
    def GetData(self):
        modelData = list(map(self.ApplyMappings, self.data.tolist()))

        finalDataX = [] # list of all sandwich encoded by ID
        finalDataY = [] # list of all age and gender encoded by ID

        for entry in modelData:
            for sandID in entry[0]:
                finalDataX.append([entry[1], entry[2]])
                finalDataY.append(sandID)

        return (self.sandMappings, self.ageMappings, self.genderMappings), np.array(finalDataX).astype(np.float16), np.array(finalDataY).astype(np.float16)
    
if __name__ == '__main__':
    man = DataManager()
    print(man.GetData())