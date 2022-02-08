import cv2, os
import time
from PIL import Image
import pytesseract
from shutil import rmtree
from pathlib import Path
import stanza
from collections import Counter
import operator 


max_sec = 10 #cantidad de segundos de video analizado

if(os.path.exists("logs")):
    pass
else: os.mkdir("logs")



if(os.path.exists("aux")):
    rmtree("aux")
else: pass

if(os.path.exists("videos")):
    print("Analizando videos")
    pass
else: 
    os.mkdir("videos")
    print("Adjunte videos en la carpeta")


path_videos = os.listdir("videos")

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
                if(cnt>=max_sec):
                    break
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
    print("Completado: ",video)

print("Analizando texto extraído y creando top 5")

path_log = os.listdir("logs")

for logfile in path_log:
    with open('logs/'+logfile,'r') as tf:
        lines = tf.read()

    #stanza.download("es")

    nlp = stanza.Pipeline(lang='es')
    docas = nlp(lines)
    word_tokens= [token.text.lower() for sent in docas.sentences for token in sent.tokens]

    minimal_text = [word for word in word_tokens if(len(word)>3)]
    conteo = Counter(minimal_text)
    conteo_ordenado = sorted(conteo.items(),key=operator.itemgetter(1),reverse=True)

    with open('logs/'+'top5_%dseg_'%max_sec+logfile,'w') as f:
        for i,n in enumerate(conteo_ordenado):
            if(i<5):
                f.write(n[0])
                f.write("\n")
            else: break
print("Finalizado, resultados en directorio /logs/")

