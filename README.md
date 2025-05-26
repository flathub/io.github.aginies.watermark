# Objectif

Script en python pour ajouter un filigrane à une image.

## filigrane_app.py

Script en Python TK. Pour une utilisation sous Windows.

## Obtenir le .exe

* installer python sous windows https://www.python.org/downloads/?lang=fr
* installer PyInstaller
```
python -m pip install PyInstaller
```

* Aller dans le répertoire du script et taper:
```
pyinstaller --onefile --windowed filigrane_app.py
```

Le fichier **filigrane_app.exe** sera dans le répertoire **dist**

## easytag.py

Script en Python3 GTK3.
```
chmod 755 easy_tag.py
./easy_tag.py
```

##

## easy_tag.sh

Premiere version eb bash qui utilise ImageMagick.

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


# A FAIRE

Sans doute plein de choses!
