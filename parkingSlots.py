import cv2
import pickle




w,h = 80,70
try:
    with open ('ParkPos','rb') as f:
        posList = pickle.load(f)
        

except :
    posList =[]



def Click(events,x,y,flags,params):

    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate (posList):
            x1,y1 = pos
            if x1 < x < x1+w and y1 < y < y1 +h :
                posList.pop(i)
    
    with open ('ParkPos','wb') as f:
        pickle.dump(posList,f)
        


while True:

    img=cv2.imread('parking.png')
    for pos in posList:
        cv2.rectangle(img,pos,(pos[0]+w,pos[1]+h),(255,0,0),2)

    cv2.imshow('Park',img)
    cv2.setMouseCallback('Park',Click)
    cv2.waitKey(1)
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break

    