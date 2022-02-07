
from PIL import Image
import pytesseract
path_im = "test.jpeg"
img = Image.open(path_im)
img.load()

text = pytesseract.image_to_string(img,config="-l spa --oem 1 --psm 1")

with open("log_"+path_im[:-4]+"txt",'a') as log:
    log.write(text)