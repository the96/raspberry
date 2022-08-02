import cv2

cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    print('capture process')
    cap.read()
    r, img = cap.read()
    path = 'capture.jpg'
    cv2.imwrite(path, cv2.flip(img, -1))
    if(r == True):
        break
cap.release()