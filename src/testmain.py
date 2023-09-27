import datamanager
import sandwichDNN
from utils import guiLaunch

guiLaunch.OpenWeb()

dm = datamanager.DataManager()
model = sandwichDNN.SandwichModel(dm)

model.Fit()
print(model.Predict([4, 1], 3))