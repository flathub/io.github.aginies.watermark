# Goal (Objectif)

Python Application to Add a Watermark to Image(s). An expert mode is available to customize the watermark.
This application is used to combat **identity theft by securing official documents** with a watermark. For example: if you need to send your passport to subscribe to car insurance, you just need to select the image of your passport and add the watermark: "Insurance subscription." The application will add the watermark across the entire image, including the date and time. If someone uses this document for anything other than insurance, you can state that this document was sent solely for your insurance purposes.

**FR**: Application en Python pour ajouter un filigrane à une image ou des images. Un mode expert est disponible pour ajuster le filigrane. 
Cette application est utilisée pour lutter contre l'usurpation d'identité en sécurisant des documents officiels avec un filigrane. Par exemple : vous devez envoyer votre passeport pour souscrire une assurance automobile, il vous suffit de sélectionner l'image de votre passeport, et d'ajouter le filigrane : "Assurance souscrite". L'application ajoutera le filigrane sur toute l'image en ajoutant aussi la date et l'heure. Si quelqu'un utilise ce document pour autre chose qu'une assurance, vous pouvez dire que ce document a été envoyé uniquement pour votre assurance.

![image](https://raw.githubusercontent.com/aginies/watermark/refs/heads/main/images/example.jpg)

[![Demo](https://img.youtube.com/vi/bZkLoEjths0/0.jpg)](https://www.youtube.com/watch?v=bZkLoEjths0)

# LICENCE

[GPL2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

# Limitation

This tool can only used **Truetype font**, bitmap one can not be selected or used.
If your system can not display the font in the **GtkChooserDialog preview** (ie: it shows squares), the tool will not be able to use that font to watermark your image.
This tool do not show any view if you export to PDF file.

# Contribute

* You can open [Bug](https://github.com/aginies/watermark/issues) or do [PR](https://github.com/aginies/watermark/pulls)
* You can help on language support
* Any ideas is welcome

# Python requirements

This app is in Python GTK3, and is compatible with very old python3.6.

* pillow
* gobject

# watermark_app_gtk.py

Python GTK version.
* Add watermark to multiple images
* List of selected images
* Multiple Image viewer
* Default save directory is that of the first image
* Languages: EN, FR, ES
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
* Langues: EN, FR, ES
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

## flathub app

[![Flathub Version](https://img.shields.io/badge/watermark-4.1-blue)](https://flathub.org/apps/io.github.aginies.watermark)

### Stable version from source

To build the current latest version tarball on github:
```
make build
```
To run latest tarball version:
```
make run
```

### Devel version

To build local files
```
make localbuild
```

For more information: https://docs.flathub.org/docs/for-app-authors/submission#build-and-install

# TODO

* have a modular app not a single script
* show pdf files generated
* perhaps many more stuff....
