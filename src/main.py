# Import necessary python packages (cv2, keras, numpy)
import cv2


# Write a function that returns coordinates of face in image parameter:
def find_faces(dnn, dframe, confidence=0.9):
    
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


def Main():

    # Set up constants for the directories for the pre-trained models (face, gender, age)
    face_proto = '../data/face_proto.pbtxt'
    face_model = '../data/face_model.pb'

    gen_proto = '../data/gender_proto.prototxt'
    gen_model = '../data/gender_model.caffemodel'

    age_proto = '../data/age_proto.prototxt'
    age_model = '../data/age_model.caffemodel'

    # Load the pre-trained face dnn, gender dnn, and age dnn
    face_dnn = cv2.dnn.readNet(face_model, face_proto)
    gen_dnn = cv2.dnn.readNet(gen_model, gen_proto)
    age_dnn = cv2.dnn.readNet(age_model, age_proto)

    # Define constants for two genders and the ranges of their ages (strings)
    gender_groups = ['Male', 'Female']
    age_groups = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

    # Mean values for the DNN
    FACE_MODEL_MEAN_VALUES = [104, 117, 123]
    MODEL_MEAN_VALUES = [78.4263377603, 87.7689143744, 114.895847746]

    # Define camera width, height, padding, and open video capture stream
    width = 1080
    height = 720
    padding = 20

    cam = cv2.VideoCapture(0)

    # Do the following forever until someone presses Esc:
    while cv2.waitKey(1) < 0:
        # Get a video frame from the camera
        ready, frame = cam.read()
        if not ready:
            # If camera is not ready, continue to try to get the video frame
            continue

        # Flip the frame using opencv (cv2.flip(video, 1))
        frame = cv2.flip(frame, 1)
        # Resize the frame to specified dimensions (to fill screen)
        frame = cv2.resize(frame, (width, height))

        # Call face-coordinate function on current frame object
        dnn_frame, face_boxes = find_faces(face_dnn, frame)

        if face_boxes:
            # For each face:
            for face_box in face_boxes:
                # isolate face
                face = frame[max(0, face_box[1] - padding) : min(face_box[3] + padding, frame.shape[0] - 1),
                            max(0, face_box[0] - padding) : min(face_box[2] + padding, frame.shape[1] - 1)]
                
                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

                # Pass face object to gender dnn and store result
                gen_dnn.setInput(blob)
                gen_preds = gen_dnn.forward()
                gender = gender_groups[gen_preds[0].argmax()]
                # print(f'Gender: {gender}')

                # Pass face object to age dnn and store result
                age_dnn.setInput(blob)
                age_preds = age_dnn.forward()
                age = age_groups[age_preds[0].argmax()]
                # print(f'Age: {age} years')

                # Draw bounding box around face
                # Write age and gender above bounding box using cv2 functions
                cv2.putText(dnn_frame, f'{gender}, {age}', (face_box[0], face_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        
        # End of the face loop

        # Show the frame on the screen
        cv2.imshow('AGE DNN', dnn_frame)

    # End of the frame loop


    # Release camera
    cam.release()

    # Close the window(s)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    Main()