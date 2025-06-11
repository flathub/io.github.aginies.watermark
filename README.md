# Goal (Objectif)

Python Application to Add a Watermark to an Image or Images

**FR**: Application en python pour ajouter un filigrane à une image ou des images.

![image](https://github.com/aginies/watermark/blob/08da28cacd0612f564e3e23a19ac0b765343b820/images/example.jpg)

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

## Get the .exe (Windows)

* Install Python on Windows https://www.python.org/downloads/?lang=fr
* install MSYS2: http://www.msys2.org
* Open a Terminal:
```
* pacman -Suy
* pacman -Su mingw-w64-x86_64-python-gobject mingw-w64-x86_64-python-gtk mingw-w64-x86_64-gtk3 mingw-w64-x86_64-pyinstaller
```

* Go to the script directory and type:
```
pyinstaller.exe --onefile --windowed watermark_app_gtk.py --name watermark --splash watermark_starting.jpg -i io.github.aginies.watermark.ico
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

# OLD stuff

## easy_tag.sh (No GUI)

Premiere version en bash qui utilise ImageMagick.

### AVANT UTILISATION

* Editer le fichier **easy_tag.sh** et changer le parametre TEXTTOINCLUDE avec la valeur que vous voulez sur-imprimer sur l'image.
* rendre le fichier **easy_tag.sh** executable:
```
chmod +x easy_tag.sh
```
* installer ImageMagick

### Example

avec TEXTTOINCLUDE="SUBJECT TO TAG"

```
./easy_tag.sh ~/Pictures/test.png 
test_TAG_TO_INCLUDE_20240515.png
```

![image](https://github.com/aginies/easy_tag/blob/202f6f2a8de8fd39f0d14bc8ea4232a029f3b6d9/suse_TAG_TO_INCLUDE_20240515.jpg)

## watermark_app.py TK (version 2.0 for windows)

Basix Python TK script. Mostly built For use under Windows.
* Add watermark to multiple images
* List of selected images
* Image viewer
* Image resizing to 1280x
* JPEG compression at 75%
* Default save directory is that of the first image


**FR**:
Script en Python TK. Pour une utilisation sous Windows.
* Ajout filigrane sur de multiple images
* Liste des images selectionnées
* visualiseur d'images
* Redimension de l'image en 1280x
* Compression en JPEG à 75%
* Répertoire de sauvegarde par défaut est celui de la première image

[![Demo](https://img.youtube.com/vi/XCRIuAW7zwY/0.jpg)](https://www.youtube.com/watch?v=XCRIuAW7zwY)

# LICENCE

GPL2

# A FAIRE

Sans doute plein de choses!
