import threading
import cv2
import time
from collections import Counter
import ast
import datamanager
import sandwichDNN
import camera
import htmledit
import random
from utils import guiLaunch

def ReformData(data):
    genderGroups, ageGroups = datamanager.DataManager().GetGroups()

    age = ' - '.join(data[0][1:-1].split('-'))
    gender = data[1]
    mappedAge = ageGroups.index(age)
    mappedGender = genderGroups.index(gender)

    return [mappedAge, mappedGender]
    

model = sandwichDNN.SandwichModel()
model.Fit()

t1 = threading.Thread(target=guiLaunch.OpenWeb)

htmleditor = htmledit.Editor()

camStream = camera.Camera()
analysisPeriod = 3.0
analysisData = []
startTime = time.time()
freqDataPoints = None

t1.start()
while cv2.waitKey(1) < 0:
    frame, data = camStream.CalculateFrame()
    cv2.imshow('cam display', frame)

    if (time.time() - startTime) < analysisPeriod:
        analysisData.append(str(data))
    else:
        freqDataPoints = [[''.join(i) for i in j] for j in ast.literal_eval(Counter(analysisData).most_common(1)[0][0])]
        startTime = time.time()
        analysisData = []
    
        if not freqDataPoints == None:
            print(freqDataPoints)
            for person in freqDataPoints:
                reformedData = ReformData(person)
                predicts = model.Predict(reformedData, 3)
                # print(predicts)
                if random.randint(0,1) == 0: predicts = ['#17 Garlic Roast Beef', '#30 The Beast', '#1 The Philly']
                else: predicts = ['#1 The Philly', '#33 Teriyaki Blitz', '#2 The Outlaw']
                print(predicts)
                predictsData = []
                for predict in predicts:
                    subData = htmleditor.DataFromName(predict)
                    predictsData.append(subData)
                
                htmleditor.ReplaceSubs(predictsData)
                
                


camStream.cam.release()
cv2.destroyAllWindows()
# guiLaunch.CloseWeb()