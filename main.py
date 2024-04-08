import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import cvzone
import numpy as np
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

opkeys = ['Back', 'Enter', 'Space']

finalText = ""

keyboard = Controller()

#simple draw function
'''
def drawAll(img, buttonlist):
    for button in buttonlist:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
'''

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        if button.text in opkeys:
            cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], 2 * button.size[0], button.size[1]),
                              20, rt=0)
            cv2.rectangle(imgNew, button.pos, (x + 2 * button.size[0], y + button.size[1]),
                          (255, 0, 255), cv2.FILLED)
        else:
            cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                              20, rt=0)
            cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text



# myButton = Button([100, 100], "Q")
buttonlist = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonlist.append(Button([100 * x + 50, 100 * i + 50], key))
    buttonlist.append(Button([100 * (len(keys[i])) + 50, 100 * i + 50], opkeys[i]))

while True:
    success, img = cap.read()
    # Flip the image horizontally (180 degrees) around the x-axis
    img = cv2.flip(img, 1)  # 1 means flip horizontally (around y-axis)
    hands, img = detector.findHands(img, draw=True) # This function might automatically draw hands
    img = drawAll(img, buttonlist)
    if hands:  # If hands are detected
        # Assuming findHands or another function gives you the landmarks and bbox
        hand = hands[0]  # If multiple hands, take the first one
        lmlist = hand["lmList"]  # List of 21 Landmark points
        bbox = hand["bbox"]  # Bounding box info x,y,w,h
        centerPoint = hand['center']  # center of the hand cx,cy
        handType = hand["type"]  # Hand type Left or Right

        for button in buttonlist:
            x, y = button.pos
            w, h = button.size

            if x < lmlist[8][0] < x+w and y < lmlist[8][1] < y+h:
                cv2.rectangle(img, (x-10, y-10), (x + w+10, y + h+10), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                #when clicked
                if x < lmlist[12][0] < x + w and y < lmlist[12][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if button.text == 'Space':
                        keyboard.press(Key.space)
                        time.sleep(1)

                    elif button.text == 'Enter':
                        keyboard.press(Key.enter)
                        time.sleep(1)

                    elif button.text == 'Back':
                        keyboard.press(Key.backspace)
                        time.sleep(1)

                    else:
                        keyboard.press(button.text)
                        finalText += button.text
                        time.sleep(1)

    cv2.rectangle(img, (50, 350), (700, 450), (130, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
