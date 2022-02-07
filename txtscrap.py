
from PIL import Image
import pytesseract

img = Image.open("test.jpeg")
img.load()

text = pytesseract.image_to_string(img,config="-l spa --oem 1 --psm 1")
print(text)