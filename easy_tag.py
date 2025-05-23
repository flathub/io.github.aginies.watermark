import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
import random
import time

class FiligraneApp(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Ajout Filigrane Image")

        self.set_border_width(10)
        self.set_default_size(450, 200)

        # Create a vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # HBox for file selection: label + file chooser button
        file_hbox = Gtk.Box(spacing=6)
        file_label = Gtk.Label(label="Selection Image:")
        self.file_filechooser_button = Gtk.FileChooserButton()
        self.file_filechooser_button.set_title("Select a File")
        self.file_filechooser_button.set_action(Gtk.FileChooserAction.OPEN)

        file_hbox.pack_start(file_label, False, False, 0)
        file_hbox.pack_start(self.file_filechooser_button, True, True, 0)
        vbox.pack_start(file_hbox, False, False, 0)

        # HBox for filigrane text: label + entry
        filigrane_hbox = Gtk.Box(spacing=6)
        filigrane_label = Gtk.Label(label="Filigrane Text:")
        self.filigrane_entry = Gtk.Entry()
        self.filigrane_entry.set_text("FILIGRANE A AJOUTER")
        filigrane_hbox.pack_start(filigrane_label, False, False, 0)
        filigrane_hbox.pack_start(self.filigrane_entry, True, True, 0)
        vbox.pack_start(filigrane_hbox, False, False, 0)

        # HBox for output path selection
        output_hbox = Gtk.Box(spacing=6)
        output_label = Gtk.Label(label="Répertoire Sauvegarde:")
        self.output_filechooser_button = Gtk.FileChooserButton()
        self.output_filechooser_button.set_title("Select Output Folder")
        self.output_filechooser_button.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        output_hbox.pack_start(output_label, False, False, 0)
        output_hbox.pack_start(self.output_filechooser_button, True, True, 0)
        vbox.pack_start(output_hbox, False, False, 0)

        # Button to add filigrane
        self.add_filigrane_button = Gtk.Button(label="Génération Image")
        self.add_filigrane_button.connect("clicked", self.on_add_filigrane_clicked)
        vbox.pack_start(self.add_filigrane_button, False, False, 0)

        # Image display area
        self.image_widget = Gtk.Image()
        vbox.pack_start(self.image_widget, True, True, 0)

    def on_add_filigrane_clicked(self, widget):
        image_path = self.file_filechooser_button.get_filename()
        filigrane_text = self.filigrane_entry.get_text()

        if not image_path or not filigrane_text:
            return

        output_dir = self.output_filechooser_button.get_current_folder()

        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', 'webp')):
            output_image_path = self.add_filigrane_to_image(image_path, filigrane_text)
        else:
            print("Le fichier n'est pas une image!")

        if output_image_path and os.path.exists(output_image_path):
            self.image_widget.set_from_file(output_image_path)
        else:
            print("Echec!")

    def get_current_time_ces(self):
        now = time.time()
        cest_time = time.localtime(now + 3600)
        return cest_time

    def add_filigrane_to_image(self, image_path, text):
        try:
            with Image.open(image_path).convert("RGBA") as img:
                width_percent = (1280 / float(img.width))
                height_size = int((float(img.height) * float(width_percent)))

                if max(img.size) > 1280:
                    img = img.resize((1280, height_size), Image.ANTIALIAS)

                draw = ImageDraw.Draw(img)

                font_size = 14
                cest_time = self.get_current_time_ces()

                if os.path.exists('/usr/share/fonts/truetype/DejaVuSans-Bold.ttf'):
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
                else:
                    font = ImageFont.load_default()

                timestamp_str_text = time.strftime('%d%m%Y_%H%M%S', cest_time)
                full_filigrane_text = f"{text} {timestamp_str_text}"
                print("DEBUG:", full_filigrane_text )
                text_width, text_height = draw.textsize(full_filigrane_text, font=font)

                dpi = 11.0
                interval_pixels = int(1 * dpi)

                for y in range(interval_pixels, img.height, interval_pixels):
                    x = random.randint(0, img.width - text_width)
                    angle = random.uniform(-40, 40)

                    color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                        80
                    )

                    rotated_text_img = Image.new('RGBA', img.size)
                    draw_rotated = ImageDraw.Draw(rotated_text_img)

                    text_position = (x + text_width/2, y + text_height/2)
                    temp_image = Image.new('RGBA', (text_width * 3, text_height * 3), (0, 0, 0, 0))
                    temp_draw = ImageDraw.Draw(temp_image)
                    temp_draw.text((text_width, text_height), full_filigrane_text, font=font, fill=color)

                    rotated_text = temp_image.rotate(angle, expand=True)

                    rotated_text_position = (
                        x + text_width/2 - rotated_text.width/2,
                        y + text_height/2 - rotated_text.height/2
                    )

                    img.paste(rotated_text, (int(rotated_text_position[0]), int(rotated_text_position[1])), mask=rotated_text)

            timestamp_str = time.strftime('%d%m%Y_%H%M%S', cest_time)
            original_filename = os.path.basename(image_path)
            final_filename = f"ready_{text}_{timestamp_str}_{original_filename}.jpg"
            output_dir = self.output_filechooser_button.get_current_folder()
            if not output_dir:
                output_dir = tempfile.gettempdir()
            output_path = os.path.join(output_dir, final_filename)
            img.convert("RGB").save(output_path, "JPEG", quality=75)
            return output_path

        except Exception as err:
            print(f"Error adding filigrane: {err}")
            return None

win = FiligraneApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

