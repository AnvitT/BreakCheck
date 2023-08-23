import requests
import cv2
import numpy as np
import os
import sys
import time
import pyautogui


MinimumPercentageDifference = 5
TimeBeforeStart = 2
TimeoutLimit = 10000
TakeScreenShotinEvery__Seconds = 3
apiToken = '6372182118:AAEmyyrlHm8igUnYQkbAZh27o3oO2tUS6bI'
chatID = '5653362497'

def send_to_telegram(message):
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def checkDifferent():

    img1 = cv2.imread('ss1.jpg', 0)
    img2 = cv2.imread('ss2.jpg', 0)

    res = cv2.absdiff(img1, img2)
    res = res.astype(np.uint8)

    percentage = (np.count_nonzero(res) * 100)/ res.size
        
    if percentage >= (MinimumPercentageDifference):
        return True
    else:
        return False 

 
def removeScreenShots():
    os.remove('ss1.jpg')
    os.remove('ss2.jpg')    


def main():
    for remaining in range(TimeBeforeStart, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(remaining))
            sys.stdout.flush()
            time.sleep(1)
    # print('')
    os.system('CLS')

    before = pyautogui.screenshot()
    before.save('ss1.jpg')

    for counter in range(1,TimeoutLimit):
        current = pyautogui.screenshot()
        current.save('ss2.jpg')
        if checkDifferent():
            try:
                send_to_telegram("Break Over")
                removeScreenShots()   
                print("Sent Message!")  
                sys.exit()
            except Exception as e:
                os.system('CLS') 
                removeScreenShots()
                print(e)
                time.sleep(10)
                sys.exit()
        print("Running....")        
                
    send_to_telegram("Timeout!")
    removeScreenShots()
    print('Time Limit Exceeded!!')


if __name__ == "__main__":
    main()
