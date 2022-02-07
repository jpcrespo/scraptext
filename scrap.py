import cv2, os
import time
from PIL import Image
import pytesseract
from shutil import rmtree
from pathlib import Path


path_videos = os.listdir("videos")

if(os.path.exists("logs")):
    pass
else: os.mkdir("logs")

for video in path_videos:
    print("Procesando: ", video)
    capture = cv2.VideoCapture("videos/"+video) 
    fps = capture.get(cv2.CAP_PROP_FPS)
    cnt = 0
    time=0
    os.mkdir("aux")
    while (capture.isOpened()):
        ret, frame = capture.read()
        if (ret == True):
            if(time>fps):
                cv2.imwrite('aux/IMG_%04d.jpg' % cnt,frame)
                cnt+=1
                time=0
            else:
              time+=1
        else:
            break
    capture.release()
    cv2.destroyAllWindows()
    

    caps = os.listdir("aux")
    for path_im in caps:
        img = Image.open("aux/"+path_im)
        img.load()
        text = pytesseract.image_to_string(img,config="-l spa --oem 1 --psm 1")
        with open("logs/"+Path(video).stem+'.txt','a') as log:
            log.write(text)
    rmtree("aux")
