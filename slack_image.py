import cv2
import datetime
import time
import sys
import traceback
import requests

cap = cv2.VideoCapture(0)

token_file = open('/home/the96/program/token')
token = token_file.read()
token_file.close()
result = requests.post('https://slack.com/api/chat.postMessage', params={
    'text': 'インターホン通知を開始します', 
    'token': token, 
    'channel': 'C03R7TA1Y4A'
})
print(result.json())
try:
    while (cap.isOpened()):
        r, img = cap.read()
        if (r == False): pass
        path = '/home/the96/program/test_image.jpg'
        cv2.imwrite(path, cv2.flip(img, -1))
        files = {'file': open(path, 'rb')}
        param = {
            'token': token, 
            'channels': 'C03R7TA1Y4A',
            'filename': 'test.jpg',
            'initial_comment': 'test',
            'title': 'test'
        }
        # result = requests.post(url="https://slack.com/api/files.upload", params=param, files=files)
        print(result.json())
        break
except:
    print(traceback.format_exc())
    print('release')
    cap.release()
    sys.exit()
