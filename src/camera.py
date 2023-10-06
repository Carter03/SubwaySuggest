import cv2
import numpy as np
import sys

class Camera:
    def __init__(self, height=720, width=1080):
        # constants for the directories for the pre-trained models (face, gender, age)
        self.face_proto = '../data/face_proto.pbtxt'
        self.face_model = '../data/face_model.pb'
        self.gen_proto = '../data/gender_proto.prototxt'
        self.gen_model = '../data/gender_model.caffemodel'
        self.age_proto = '../data/age_proto.prototxt'
        self.age_model = '../data/age_model.caffemodel'

        # Load the pre-trained face dnn, gender dnn, and age dnn
        self.face_dnn = cv2.dnn.readNet(self.face_model, self.face_proto)
        self.gen_dnn = cv2.dnn.readNet(self.gen_model, self.gen_proto)
        self.age_dnn = cv2.dnn.readNet(self.age_model, self.age_proto)

        # Define constants for two genders and the ranges of their ages (strings)
        self.gender_groups = ['Male', 'Female']
        self.age_groups = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

        self.FACE_MODEL_MEAN_VALUES = [104, 117, 123]
        self.MODEL_MEAN_VALUES = [78.4263377603, 87.7689143744, 114.895847746]

        self.width = width
        self.height = height
        self.padding = 20

        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # if self.cam is None or not self.cam.isOpened():
        #     raise Exception("Camera cannot be accessed")


    # Write a function that returns coordinates of face in image parameter:
    def find_faces(self, dnn, dframe, confidence=0.9):
        # Create a local copy of the dframe and get height and width
        dnn_frame = dframe.copy()
        frame_height = dnn_frame.shape[0]
        frame_width = dnn_frame.shape[1]

        dnn_blob = cv2.dnn.blobFromImage(dnn_frame, 1.0, (300, 300), [104, 117, 123], True, False)

        dnn.setInput(dnn_blob)
        faces = dnn.forward()

        face_boxes = []
        
        for i in range(faces.shape[2]):

            dnn_confidence = faces[0, 0, i, 2]

            if dnn_confidence > confidence:
                x1 = int(faces[0, 0, i, 3] * frame_width)
                y1 = int(faces[0, 0, i, 4] * frame_height)

                x2 = int(faces[0, 0, i, 5] * frame_width)
                y2 = int(faces[0, 0, i, 6] * frame_height)


                face_boxes.append([x1, y1, x2, y2])
                cv2.rectangle(dnn_frame, (x1, y1), (x2, y2), (255, 0, 0), int(round(frame_height / 150)), 8)

        return dnn_frame, face_boxes
    
    def GetSharpness(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(img, cv2.CV_16S)
        mean, stddev = cv2.meanStdDev(lap)
        return stddev[0,0]


    def CalculateFrame(self):
        # Get a video frame from the camera
        ready, frame = self.cam.read()
        if not ready or not self.cam.isOpened():
            print("\n\nCamera Disconnected During Application Run")
            sys.exit(1)
        
        if self.GetSharpness(frame) > 100:
            print("\n\nImage Sharpness Detected Too High. Possible Camera Error. Ensure No Other Applications Are Using The Camera")
            sys.exit(1)

        # Flip the frame using opencv (cv2.flip(video, 1))
        frame = cv2.flip(frame, 1)
        # Resize the frame to specified dimensions (to fill screen)
        frame = cv2.resize(frame, (self.width, self.height))

        # Call face-coordinate function on current frame object
        dnn_frame, face_boxes = self.find_faces(self.face_dnn, frame)
        peopleData = []

        if face_boxes:
            # For each face:
            for face_box in face_boxes:
                # isolate face
                face = frame[max(0, face_box[1] - self.padding) : min(face_box[3] + self.padding, frame.shape[0] - 1),
                            max(0, face_box[0] - self.padding) : min(face_box[2] + self.padding, frame.shape[1] - 1)]
                
                if face.size:
                    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)

                    # Pass face object to gender dnn and store result
                    self.gen_dnn.setInput(blob)
                    gen_preds = self.gen_dnn.forward()
                    gender = self.gender_groups[gen_preds[0].argmax()]

                    # Pass face object to age dnn and store result
                    self.age_dnn.setInput(blob)
                    age_preds = self.age_dnn.forward()
                    age = self.age_groups[age_preds[0].argmax()]

                    # Draw bounding box around face
                    # Write age and gender above bounding box using cv2 functions
                    cv2.putText(dnn_frame, f'{gender}, {age}', (face_box[0], face_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                    peopleData.append((age, gender))

        return dnn_frame, peopleData
            

if __name__ == '__main__':
    obj = Camera()

    while cv2.waitKey(1) < 0:
        cv2.imshow('test', obj.CalculateFrame()[0])
    
    obj.cam.release()
    cv2.destroyAllWindows()
