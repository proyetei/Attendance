import cv2
import os
import numpy as np
import pickle
import face_recognition
import cvzone
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
print("hello world")
imgBackground = cv2.imread('Resources/background.png')

# add a path and then for loop for importing the images for the 4 different modes into a list
# MODES: active, marked, already marked, scanning the student
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path))) 
# load the encoding file

file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")
# run the webcam
while True:
    success, img = cap.read()
    
    # scale image down to 1/4 of the size
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]
    
    for encoFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            print("Known face detected!")
            studentIds[matchIndex]
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162 + y1, x2 - x1, y2 - y1 # show a rectangle which moves along with your face
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0)
            
    cv2.imshow("Face Attendance", imgBackground) 
    cv2.waitKey(1)
    

print("hello world")