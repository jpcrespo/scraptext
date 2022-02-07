# Scraptext

Este proyecto contiene la siguiente raiz:
  
        - scrap.py
  
Cuando se corre por primera vez crea una carpeta \<\<videos>> donde se deben cargar los videos a analizar. Al volver a correr scrap.py va analizando uno a uno los videos del directorio.


1. scrap.py crea temporalmente la carpeta \<\<aux>> donde guarda un fotograma por cada segundo de video. Posteriormente analiza cada imagen reconociendo el texto para escribirlo en un archivo de texto plano con el mismo nombre del video analizado. Una vez finalizado el análisis borra la carpeta.

2. scrap.py genera como resultado un archivo de texto plano con el texto reconocido en el video. Este se almacena en la carpeta \<\<logs>> bajo el mismo nombre del video.

Para poder utilizar el script se debe tener instalado dos frameworks:
   - OpenCV.
   - Tesseract.

En Debian se instalan con:

``` sh
sudo apt install tesseract-ocr-spa
sudo apt install libgtk2.0-dev 
sudo apt install libopencv-dev
```
Adicionalmente los paquetes:
``` sh
pip install pytesseract
```
Para correr el programa:
``` sh
python scrap.py
```
