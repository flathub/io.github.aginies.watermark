# Goal (Objectif)

Python Application to Add a Watermark to Image(s). An expert mode is available to customize the watermark.
This application is used to combat **identity theft by securing official documents** with a watermark. For example: if you need to send your passport to subscribe to car insurance, you just need to select the image of your passport and add the watermark: "Insurance subscription." The application will add the watermark across the entire image, including the date and time. If someone uses this document for anything other than insurance, you can state that this document was sent solely for your insurance purposes.

**FR**: Application en python pour ajouter un filigrane à une image ou des images. Un mode expert est disponibl pour ajuster le filigrane.
Cette application est utilise pour lutter contre  l'usurpation d'identité en sécurisant des documents officiels avec un filigrane. Par example: vous devez envoyer votre passeport pour souscrire une assurance automobile, il vous suffit de séléctionner l'image de votre passport, et rajouter le filigrane: "Assurance souscrire". L'application rajoutera le filigrane sur toute l'image en ajoutant aussi la date et l'heure. Si quelqu'un utilise ce document pour autre chose qu'une assurance, vous pouvez dire que ce document a été envoyé uniquement pour votre assurance.

![image](https://github.com/aginies/watermark/blob/873fd84710295287ff2bf266b40a714bcc84a2a7/images/example.jpg)

[![Demo](https://img.youtube.com/vi/rNg0RGUvESI/0.jpg)](https://www.youtube.com/watch?v=rNg0RGUvESI)

# Python requirements

* pillow
* gobject

# watermark_app_gtk.py

Python GTK version.
* Add watermark to multiple images
* List of selected images
* Multiple Image viewer
* Default save directory is that of the first image
* Expert mode: 
  * font selection
  * font color choice or random
  * font transparency
  * text angle
  * density
  * optionnal Date + Hour
  * filename prefix
  * JPG compression level
  * Image resize

**FR**:
Script en Python GTK.
* Ajout filigrane sur de multiple images
* Liste des images selectionnées
* Visualiseur d'images
* Répertoire de sauvegarde par défaut est celui de la première image
* Expert mode: 
  * séléction font
  * couleur font ou via le hasard
  * transparence font
  * angle du texte
  * option date + Heure
  * prefix de nom de fichier
  * densité
  * niveau de compression JPEG
  * taille image

## Use directly

```
git clone https://github.com/aginies/watermark.git
cd watermark
python3 watermark_app_gtk.py
```

## Get the .exe (Windows)

* Install Python on Windows https://www.python.org/downloads/?lang=fr
* install MSYS2: http://www.msys2.org
* Open a MSYS2 64b Terminal:
```
* pacman -Suy
* pacman -Su mingw-w64-x86_64-python-gobject mingw-w64-x86_64-python-gtk mingw-w64-x86_64-gtk3 mingw-w64-x86_64-pyinstaller
```

* Go to the script directory and type:
```
pyinstaller.exe --onefile --windowed watermark_app_gtk.py --name watermark --splash watermark_starting.jpg -i io.github.aginies.watermark.ico --version-file="version.txt"
```

The **watermark.exe** file will be in the **dist** directory.
To get a version with console debug, you need to remove the **--windowed** option from the **pyinstaller** command.

## flathub app (TOFIX)

To build the current latest version tarballon github:
```
make build
```

To build local files
```
make localbuild
```

To run latest tarball version:
```
make run
```

For more information: https://docs.flathub.org/docs/for-app-authors/submission#build-and-install

# LICENCE

GPL2

# A FAIRE

Sans doute plein de choses!
