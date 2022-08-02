import cv2
import datetime
import time
import sys
import traceback
import requests
import json

def check_image(gray1, gray2, gray3):
    diff1 = cv2.absdiff(gray1, gray2)
    diff2 = cv2.absdiff(gray2, gray3)

    diff_and = cv2.bitwise_and(diff1, diff2)

    _, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)
    return diff_wb

cap = cv2.VideoCapture(0)
r, img = cap.read()
img1  = img2  = img3  = img
gray1 = gray2 = gray3 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

token_file = open('/home/the96/program/token','r')
token = token_file.read()
token_file.close()

now = datetime.datetime.now()
log_file_path = '/home/the96/intercome_log/txt/'+now.strftime('%Y-%m-%d-%H-%M-%S-%f')+'.log'
def write_log(logstr):
    timestamp = datetime.datetime.now()
    log_file = open(log_file_path, 'a')
    log_file.write(timestamp.strftime('%Y-%m-%d-%H-%M-%S-%f: ') + logstr + '\n')
    log_file.close()

try:
    
    result = requests.post('https://slack.com/api/chat.postMessage', params={
        'text': 'インターホン通知を開始します', 
        'token': token, 
        'channel': 'C03R7TA1Y4A'
    })
    write_log(json.dumps(result.json()))
    while (cap.isOpened()):
        r, img = cap.read()
        if (r == False): pass

        img2,  img3  = (img1,  img2 )
        gray2, gray3 = (gray1, gray2)
        img1  = img
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

        diff_img = check_image(gray1, gray2, gray3)
        diff = cv2.countNonZero(diff_img)
        if (diff > 5000):
            now = datetime.datetime.now()
            write_log(now.strftime('%Y-%m-%d %H:%M:%S.%f') + ': diff ' + str(diff))
            result = requests.post('https://slack.com/api/chat.postMessage', params={
                'text': 'インターホンが鳴りました', 
                'token': token, 
                'channel': 'C03R7TA1Y4A'
            })
            write_log(json.dumps(result.json()))

            time.sleep(4.5)
            _, log_img = cap.read()

            path_base = '/home/the96/intercome_log/image/' + now.strftime('%Y-%m-%d-%H-%M-%S-%f')
            log_1 = path_base + '_1.jpg'
            cv2.imwrite(path, cv2.flip(img1, -1))

            log_2 = path_base + '_2.jpg'
            cv2.imwrite(path, cv2.flip(img2, -1))

            log_3 = path_base + '_3.jpg'
            cv2.imwrite(path, cv2.flip(img3, -1))
            
            log_img = path_base + '.jpg'
            cv2.imwrite(path, cv2.flip(log_img, -1))

            files = {'file': open(path, 'rb')}
            param = {
                'token': token, 
                'channels': 'C03R7TA1Y4A',
                'filename': 'intercome log',
                'initial_comment': '',
                'title': 'intercome log '+ now.strftime('%Y-%m-%dT%H:%M:%S')
            }
            result = requests.post(url="https://slack.com/api/files.upload", params=param, files=files)
            write_log(json.dumps(result.json()))
            time.sleep(30)
        time.sleep(1)
except:
    write_log(traceback.format_exc())
    requests.post('https://slack.com/api/chat.postMessage', params={
        'text': 'インターホン通知を終了します', 
        'token': token, 
        'channel': 'C03R7TA1Y4A'
    })
    cap.release()
    sys.exit()
