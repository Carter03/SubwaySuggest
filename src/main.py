import threading
import cv2
import sandwichDNN
import camera
from utils import guiLaunch

# def OpenInBrowser():
#     guiLaunch.OpenWeb() # blocking main thread :(

# def Test2():
#     model = sandwichDNN.SandwichModel()

#     model.Fit()
#     print(model.Predict([4, 1], 3))

# t1 = threading.Thread(target=OpenInBrowser)
# t2 = threading.Thread(target=Test2)

# t1.start()
# t2.start()

t1 = threading.Thread(target=guiLaunch.OpenWeb)

camStream = camera.Camera()

t1.start()
while cv2.waitKey(1) < 0:
    frame, data = camStream.CalculateFrame()
    cv2.imshow('cam display', frame)

camStream.cam.release()
cv2.destroyAllWindows()