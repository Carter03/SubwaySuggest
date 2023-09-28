import threading
import cv2
import time
from collections import Counter
import ast
import datamanager
import sandwichDNN
import camera
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
                print(model.Predict(reformedData, 3))


camStream.cam.release()
cv2.destroyAllWindows()
t1.close()