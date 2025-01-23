import cv2
import numpy as np

def detect_color(frame, lowerHSV, upperHSV):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerHSV, upperHSV)
    detect = np.where(mask > 0)

    kernel = np.ones((5, 5), np.uint8) #what if uint16 instead? or even 32 bits? What happens?

    img = cv2.bitwise_and(frame, frame, mask=mask) #mask for black spaces
    img = cv2.erode(img, kernel, iterations=1) #remove pixels
    img = cv2.dilate(img, kernel, iterations=1) #add them to boundary
    img = cv2.Canny(img, 40, 180) 

    if len(detect) > 0 and len(detect[1]):
        print(detect[0].min(), detect[0].max())
        print(detect[1].min(), detect[1].max()) 

        midPoint = ((detect[1].min()+detect[1].max())//2, (detect[0].min() + detect[0].max()) // 2)
        midPoint2 = (int(detect[1].mean()), int(detect[0].mean()))
        color = (0, 0, 255) 
        color2 = (0, 255, 255)
        cv2.circle(img, midPoint, 7, color, 2) #
        cv2.circle(img, midPoint2, 12, color2, 2)

    return img

if __name__ == "__main__":
    #color range (opencv HSV)
    lower_ball = np.array([79, 0, 0])
    upper_ball = np.array([84, 220, 157])

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        result = detect_color(frame, lower_ball, upper_ball)

        cv2.imshow('original frame', frame)
        cv2.imshow('result', result)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()