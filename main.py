import cv2
import numpy as np
import cvzone
import pickle

#VideoRead

cap= cv2.VideoCapture('ParkingVideo.mp4')



frame_w= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_y=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps=int(cap.get(cv2.CAP_PROP_FPS)/3)
size=(frame_w,frame_y)

video_filename='ParkingSlots.mp4'

video_output=cv2.VideoWriter(video_filename,cv2.VideoWriter_fourcc(*'XVID'),fps,size)


with open ('ParkPos','rb') as f:
        posList = pickle.load(f)

w,h = 80,70




def DrawParkingRectangle(imgPro):
     
     for pos in posList:
        x,y = pos
    
        imgCrop= imgPro[y:y+h,x:x+w]
        #cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+h-5), scale= 0.8, thickness= 1,offset= 0)

        if count < 600:
             color = (0,255,0)
             thickness= 4
        
        else:
             color = (0,0,255)
             thickness= 2

        cv2.rectangle(img,pos,(pos[0]+w,pos[1]+h),color,thickness)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    succes,img = cap.read()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur= cv2.GaussianBlur(imgGray,(3,3),1)
    imgThres= cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedian=cv2.medianBlur(imgThres,5)
    kernel = np.ones((3,3), np.uint8)

    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)

    DrawParkingRectangle(imgDilate)

    #for pos in posList:
    cv2.imshow('Parking',img)
    #cv2.imshow('Median',imgMedian)
    
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break

    video_output.write(img)

cap.release()
video_output.release()
cv2.destroyAllWindows()
            
