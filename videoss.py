import cv2, os
import time

capture = cv2.VideoCapture('test.mp4') 

fps = capture.get(cv2.CAP_PROP_FPS)

cnt = 0
time=0
while (capture.isOpened()):
    ret, frame = capture.read()
    if (ret == True):
        if(time>fps):
            cv2.imwrite('IMG_%04d.jpg' % cnt,frame)
            cnt+=1
            time=0
        else:
            time+=1
    else:
        break


capture.release()
cv2.destroyAllWindows()