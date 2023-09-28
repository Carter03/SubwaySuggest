import sandwichDNN
from utils import guiLaunch

guiLaunch.OpenWeb() # blocking main thread :(

model = sandwichDNN.SandwichModel()

model.Fit()
print(model.Predict([4, 1], 3))