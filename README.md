# Objectif

Divers scripts en python pour ajouter un filigrane à une image.

## filigrane_app.py

Script en Python TK. Pour une utilisation sous Windows.
* Ajout du filigrane sur l'image
* Redimension de l'image en 1280x
* Compression en JPEG à 75%
* Support conversion multiple images
* Répertoire de sauvegarde par défaut est celui de la première image

![image](https://github.com/aginies/easy_tag/blob/555160b92cffaeda17972068ce4b4d2828de350f/filigrane_app.jpg)

## Obtenir le .exe (Windows)

* installer python sous windows https://www.python.org/downloads/?lang=fr
* installer PyInstaller
```
python -m pip install PyInstaller
```

* Aller dans le répertoire du script et taper:
```
pyinstaller --onefile --windowed filigrane_app.py
```

Le fichier **filigrane_app.exe** sera dans le répertoire **dist**.
Pour obtenir une version avec du debug de console il faut retirer l'option **--windowed** de la commande **pyinstaller**.

## easytag.py (obsolete)

Script en Python3 GTK. Version initiale mais impossible de le faire fonctionner sous Windows,
donc j'ai fait une version avec TK. Cette version n'est plus la maintenue pour privilégié
une version mult- plateforme (avec TK).
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
