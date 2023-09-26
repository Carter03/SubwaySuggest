import datamanager
import sandwichDNN

dm = datamanager.DataManager()
model = sandwichDNN.Model(dm)

model.Fit()

print(model.Predict([4, 1], 3))