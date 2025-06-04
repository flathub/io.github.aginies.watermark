# Goal (Objectif)

Python Application to Add a Watermark to an Image or Images

**FR**: Application en python pour ajouter un filigrane à une image ou des images.

# watermark_app.py

Python TK script. For use on Windows or Linux.
* Add watermark to multiple images
* List of selected images
* Image viewer
* Image resizing to 1280x
* JPEG compression at 75%
* Default save directory is that of the first image


**FR**:
Script en Python TK. Pour une utilisation sous Windows ou Linux.
* Ajout filigrane sur de multiple images
* Liste des images selectionnées
* visualiseur d'images
* Redimension de l'image en 1280x
* Compression en JPEG à 75%
* Répertoire de sauvegarde par défaut est celui de la première image

[![Demo](https://img.youtube.com/vi/XCRIuAW7zwY/0.jpg)](https://www.youtube.com/watch?v=XCRIuAW7zwY)

## Get the .exe (Windows)

* Install Python on Windows https://www.python.org/downloads/?lang=fr
* Install PyInstaller
```
python -m pip install PyInstaller
```

* Go to the script directory and type:
```
pyinstaller --onefile --windowed watermark_app.py
```

The **watermark_app.exe** file will be in the **dist** directory.
To get a version with console debug, you need to remove the **--windowed** option from the **pyinstaller** command.

## flathub app

To build it:
```
make build
```

To run it:
```
make run
```

For more information: https://docs.flathub.org/docs/for-app-authors/submission#build-and-install

# OLD stuff

## easytag.py (obsolete)

Script en Python3 GTK. Version initiale mais impossible de le faire fonctionner sous Windows,
donc j'ai fait une version avec TK. Cette version n'est plus la maintenue pour privilégier
une version multi-plateforme (avec TK).
```
chmod 755 easy_tag.py
./easy_tag.py
```

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

# LICENCE

GPL2

# A FAIRE

Sans doute plein de choses!
