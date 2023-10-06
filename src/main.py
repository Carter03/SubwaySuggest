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
import cashier

def ReformData(data):
    genderGroups, ageGroups = datamanager.DataManager().GetGroups()

    age = ' - '.join(data[0][1:-1].split('-'))
    gender = data[1]
    mappedAge = ageGroups.index(age)
    mappedGender = genderGroups.index(gender)

    return [mappedAge, mappedGender]
    

model = sandwichDNN.SandwichModel()
model.Fit()

log = cashier.Logger(r'..\data\SandwichPrefsData.xlsx', r'..\data\Subdata.xlsx', datamanager.DataManager().GetGroups()[1])

guiLaunch.Init()

t1 = threading.Thread(target=guiLaunch.OpenWeb)
t2 = threading.Thread(target=log.ContinuouslyLog)
t1.setDaemon(True)
t2.setDaemon(True)

htmleditor = htmledit.Editor()

camStream = camera.Camera()
analysisPeriod = 3.5
analysisData = []
startTime = time.time()
freqDataPoints = None

t1.start()
t2.start()


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
            if (pointsLen := len(freqDataPoints)) == 0:
                responseNums = None
            elif pointsLen == 1:
                responseNums = [4]
            elif pointsLen == 2:
                responseNums = [2, 2]
            elif pointsLen == 3:
                responseNums = [2, 1, 1]
            elif pointsLen == 4:
                responseNums = [1, 1, 1, 1]
            else:
                # more than four faces
                responseNums = [1, 1, 1, 1]

            if responseNums != None:
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

                dealsData = deals.GetDeals(len(responseNums))
            else:
                predictsData = [['Recommended Sub', 'A sub customized for you will be shown here.', '0.00'] for i in range(4)]
                dealsData = deals.GetDeals(5)
                
            htmleditor.ReplaceSubs(predictsData)

            random.seed(str(freqDataPoints))
            condDeals = random.sample(dealsData, 3)
            htmleditor.ReplaceDeals(condDeals)

            guiLaunch.Reload()
                
camStream.cam.release()
cv2.destroyAllWindows()
guiLaunch.CloseWeb()