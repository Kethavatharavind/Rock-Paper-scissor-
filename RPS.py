#package are required
import random
import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
# capture video
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
#detecting the hand
detector = HandDetector(maxHands=1)
#declaring the value
timer = 0
stateResult = False
startGame = False
score = [0,0]
# tacking the background image
class Resources:
    pass


while True:
    image = cv2.imread("Resources/Background.png")
    success, img = cap.read()
# adjusting the size of camera
    imgresize = cv2.resize(img, (0, 0), None, 0.95, 0.95)
    imgresize = imgresize[:,80:480]

    # finding hands
    hands, img = detector.findHands(imgresize)

    if startGame:
        if stateResult is False:
            timer = time.time()-initialTime
            cv2.putText(image,str(int(timer)),(507,467),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),2)

        if timer>3:
            stateResult = True
            timer = 0

            if hands:
                playerMove = None
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [0,0,0,0,0]:
                    playerMove = 1
                if fingers == [1,1,1,1,1]:
                    playerMove = 2
                if fingers == [0,1,1,0,0]:
                    playerMove = 3

                randomNumber = random.randint(1,3)
                imgpc = cv2.imread(f'Resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                image = cvzone.overlayPNG(image,imgpc,(69,250))


                #scoring of player
                if (playerMove == 1 and randomNumber == 3) or \
                    (playerMove == 2 and randomNumber == 1) or\
                    (playerMove == 3 and randomNumber == 2) :
                    score[1] += 1

                #scoring of computer

                if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                    score[0] += 1


    #adjjusting the camera in background image
    image[235:691, 586:986] = imgresize


    #computer image of rock , paper and scissor
    if stateResult :
        image = cvzone.overlayPNG(image, imgpc, (60, 264))


    #score display position ,font size ,colour and thickness
    cv2.putText(image, str(score[0]), (368, 198), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
    cv2.putText(image, str(score[1]), (823, 198), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)

#camera
    cv2.imshow("ROCK PAPER SCISSORS", image)

#setting key to start the game
    key = cv2.waitKey(1)
    # S is the key to start game
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    #setting the q key to stop the game 
    if key == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break
