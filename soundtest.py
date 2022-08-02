import time
import datetime
import sys
import RPi.GPIO as GPIO
import requests

INPUT = 4
LED = 5
GPIO.setmode(GPIO.BCM)

GPIO.setup(INPUT, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

count = 0
requests.post('https://hooks.slack.com/services/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', json={'text': 'インターホン通知を開始します'})

try:
    while True:
        state = GPIO.input(INPUT)
        if state != 0:
            now = datetime.datetime.now()
            print(now, state, count)
            count = count + 1
            requests.post('https://hooks.slack.com/services/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', json={'text': 'インターホンが鳴りました'})
            time.sleep(5)
        time.sleep(0.05)
except KeyboardInterrupt:
    requests.post('https://hooks.slack.com/services/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', json={'text': 'インターホン通知を終了します'})
    GPIO.cleanup()
    sys.exit()
