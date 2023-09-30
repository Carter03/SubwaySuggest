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
import guiLaunch
import deals

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
analysisPeriod = 5.0
analysisData = []
startTime = time.time()
freqDataPoints = None

t1.start()

while cv2.waitKey(1) < 0:
    frame, data = camStream.CalculateFrame()
    cv2.imshow('Employee Display', frame)

    if (time.time() - startTime) < analysisPeriod:
        analysisData.append(str(data))
    else:
        freqDataPoints = [[''.join(i) for i in j] for j in ast.literal_eval(Counter(analysisData).most_common(1)[0][0])]
        startTime = time.time()
        analysisData = []
    
        if not freqDataPoints == None:            
            responseNums = []
            if pointsLen := len(freqDataPoints) == 1:
                responseNums = [4]
            elif pointsLen == 2:
                responseNums = [2, 2]
            elif pointsLen == 3:
                responseNums = [2, 1, 1]
            else:
                responseNums = [1, 1, 1, 1]
            
            usedSubs = []
            for person, responseNum in zip(freqDataPoints, responseNums):
                reformedData = ReformData(person)
                predicts = model.Predict(reformedData, 5)
                
                numAdded = 0
                for i in range(5):
                    if not predicts[i] in usedSubs and numAdded < responseNum:
                        usedSubs.append(predicts[i])
                        numAdded += 1
            
            predictsData = []
            for sub in usedSubs:
                subData = htmleditor.DataFromName(sub)
                predictsData.append(subData)
                
            htmleditor.ReplaceSubs(predictsData)
            dealsData = deals.GetDeals(len(freqDataPoints))

            random.seed(str(freqDataPoints))
            condDeals = random.sample(dealsData, 3)

            htmleditor.ReplaceDeals(condDeals)

            guiLaunch.Reload()
                
camStream.cam.release()
cv2.destroyAllWindows()