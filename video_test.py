import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)
cap.set(cv2.CAP_PROP_FOCUS, 0)
while(cap.isOpened()):
    print('capture process')
    cap.read()
    r, img = cap.read()
    path = 'capture.jpg'
    cv2.imwrite(path, cv2.flip(img, -1))
    if(r == True):
        break
cap.release()