#!/usr/bin/python3
# antoine@ginies.org
import os
import random
import time
import gettext
import subprocess
import gi
from PIL import Image, ImageDraw, ImageFont
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, Pango, GLib, Gdk

gettext.install('watermark_app_gtk', localedir='locale')

class WarningDialog:
    def __init__(self, title=None, message="", parent=None):
        self.title = title or "Warning"
        self.message = message
        self.parent = parent
        self.dialog = None

    def show(self):
        # Create the warning dialog if it doesn't exist yet
        if not self.dialog:
            self.dialog = Gtk.MessageDialog(
                transient_for=self.parent,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text=self.title
            )
            self.dialog.format_secondary_text(self.message)
            self.dialog.set_default_size(400, 200)

        # Show the dialog and wait for response
        response = self.dialog.run()

        if response == Gtk.ResponseType.OK:
            self.hide()

    def hide(self):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

class ImageViewerWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Image Viewer")
        self.set_default_size(800, 600)

        # Create a vertical box to hold widgets
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

        # Create a label for displaying the file path
        self.file_label = Gtk.Label()
        self.vbox.pack_start(self.file_label, False, False, 0)

        # Initialize image_label as None (will be created when an image is loaded)
        self.image_label = None

        # Track images and current index
        self.images = []
        self.current_index = -1

        # Create a horizontal box for navigation controls
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.vbox.pack_start(self.hbox, False, False, 0)

        # Previous button
        self.prev_button = Gtk.Button(label="Previous")
        self.prev_button.connect("clicked", self.on_previous_clicked)
        self.hbox.pack_start(self.prev_button, True, True, 6)

        # Index label
        self.index_label = Gtk.Label()
        self.hbox.pack_start(self.index_label, False, False, 6)

        # Next button
        self.next_button = Gtk.Button(label="Next")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.hbox.pack_start(self.next_button, True, True, 6)

    def load_images(self, image_paths):
        """Load a list of images to view"""
        self.images = image_paths
        self.current_index = 0 if len(image_paths) > 0 else -1

        # Update buttons state and index label
        self.update_buttons_state()
        self.update_index_label()

        # Display the first image if available
        if len(self.images) > 0:
            self.display_single_image(self.images[self.current_index])

    def display_single_image(self, image_path):
        """Display a single image in the window"""
        # Load the image using GdkPixbuf
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
        scaled_pixbuf = pixbuf.scale_simple(800, 600, GdkPixbuf.InterpType.HYPER)

        if hasattr(self, 'image_label') and self.image_label is not None:
            # Remove the old image label from its container
            self.vbox.remove(self.image_label)
            self.image_label = None

        # Create a new GTK Image widget with the scaled pixbuf
        self.image_widget = Gtk.EventBox()
        self.image_label = Gtk.Image.new_from_pixbuf(scaled_pixbuf)

        # Add image label to event box (to catch events on it)
        self.image_widget.add(self.image_label)

        # Connect right-click event to show context menu
        self.image_widget.connect("button-press-event", self.on_image_right_click)

        self.file_label.set_text(image_path)
        self.vbox.pack_start(self.image_widget, True, True, 0)
        self.show_all()

    def update_buttons_state(self):
        """Enable or disable navigation buttons based on current index"""
        if self.current_index == 0:
            self.prev_button.set_sensitive(False)
        else:
            self.prev_button.set_sensitive(True)

        if self.current_index == len(self.images) - 1:
            self.next_button.set_sensitive(False)
        else:
            self.next_button.set_sensitive(True)

    def update_index_label(self):
        """Update the index label to show current image number and total images"""
        total_images = len(self.images)
        if total_images > 0:
            self.index_label.set_text(f"{self.current_index + 1}/{total_images}")
        else:
            self.index_label.set_text("0/0")

    def on_previous_clicked(self, widget):
        """Handle Previous button click"""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_single_image(self.images[self.current_index])
            self.update_buttons_state()
            self.update_index_label()

    def on_next_clicked(self, widget):
        """Handle Next button click"""
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.display_single_image(self.images[self.current_index])
            self.update_buttons_state()
            self.update_index_label()

    def on_image_right_click(self, widget, event):
        """Handle right-click event on the image"""
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            # Create context menu
            menu = Gtk.Menu()

            # Add "Save" option to menu
            save_item = Gtk.MenuItem(label="Save Image as")
            save_item.connect("activate", self.on_save_activated)
            menu.append(save_item)

            # Show the menu
            menu.show_all()
            menu.popup_at_pointer(event)

    def on_save_activated(self, widget):
        """Handle the Save option selection"""
        current_image_path = self.images[self.current_index]
        dialog = Gtk.FileChooserDialog(
            title="Save Image As",
            action=Gtk.FileChooserAction.SAVE,
        )

        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Save", Gtk.ResponseType.ACCEPT)

        # Set the default file name to the current image name
        dialog.set_current_name(Gio.file_new_for_path(current_image_path).get_basename())
        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            save_path = dialog.get_filename()
            try:
                # Copy the current image to the selected location
                source_file = Gio.File.new_for_path(current_image_path)
                destination_file = Gio.File.new_for_path(save_path)
                source_file.copy(
                    destination_file,
                    Gio.FileCopyFlags.OVERWRITE,
                    None,
                    None
                )
                print(f"Image saved to {save_path}")
            except Exception as err:
                print(f"Error saving image: {err}")

        dialog.destroy()

class WatermarkApp(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title=_("Watermark App"))
        self.set_default_size(210, 70)
        self.output_folder_path = ""
        self.compression_rate = 75
        self.font_size = 20
        self.font_base_name = None
        self.watermak_prefix = ""
        self.fili_density = 140
        self.rotation_angle = 30
        self.selected_files_path = []
        self.all_images = []
        self.current_image_index = 0
        self.image_paths = ""

        # Create main vertical box container
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.add(self.vbox)

        # Setup menu bar
        menubar = Gtk.MenuBar()
        menubar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        menubar_box.pack_start(menubar, False, False, 3)
        self.vbox.pack_start(menubar_box, False, False, 3)

        # Create a "Pref" menu item
        pref_menu_item = Gtk.MenuItem(label="Preferences")
        menubar.append(pref_menu_item)
        pref_menu = Gtk.Menu()

        # Create a check menu item to toggle expert options
        self.expert_options_check = Gtk.CheckMenuItem(label="Show Expert Options")
        self.expert_options_check.connect("toggled", self.on_expert_toggle)
        self.expert_options_check.set_active(False)
        pref_menu.append(self.expert_options_check)

        # Create a check menu item to toggle Auto save Images options
        #self.autosave_options_check = Gtk.CheckMenuItem(label="Auto Save Images")
        #self.autosave_options_check.set_active(True)
        #pref_menu.append(self.autosave_options_check)

        # Attach the menu to the "View" menu item
        pref_menu_item.set_submenu(pref_menu)

        # Create "About" menu with cascading items
        about_menu_item = Gtk.MenuItem(label=_("About App"))
        about_menu = Gtk.Menu()
        about_menu_item.set_submenu(about_menu)
        menubar.append(about_menu_item)

        # Add "About Filigrane App" to the About menu
        about_filigrane_menu_item = Gtk.MenuItem(label=_("About Watermark App"))
        about_filigrane_menu_item.connect("activate", self.about_dialog)
        about_menu.append(about_filigrane_menu_item)

        button_size_group = Gtk.SizeGroup.new(Gtk.SizeGroupMode.HORIZONTAL)

        # File selection horizontal box (label + file chooser button)
        file_hbox = Gtk.Box(spacing=3)
        file_label_text = _("Select Image File(s)")
        file_label = Gtk.Label(label=file_label_text, halign=Gtk.Align.START)
        self.file_chooser_button = Gtk.Button(label="Choose Files")
        self.file_chooser_button.connect("clicked", self.on_files_clicked)
        button_size_group.add_widget(self.file_chooser_button)
        file_hbox.pack_start(file_label, False, False, 12)
        file_hbox.pack_end(self.file_chooser_button, False, False, 12)
        self.vbox.pack_start(file_hbox, False, False, 3)

        self.files_selected_hbox = Gtk.Box(spacing=3)
        self.files_label = Gtk.Label()
        self.files_selected_hbox.pack_start(self.files_label, False, False, 3)
        self.vbox.pack_start(self.files_selected_hbox, False, False, 3)

        # Watermark text horizontal box (label + entry)
        watermark_hbox = Gtk.Box(spacing=3)
        watermark_label = Gtk.Label(label=_("Watermark Text"))
        self.watermark_entry = Gtk.Entry()
        self.watermark_entry.set_placeholder_text(_("Watermark text"))
        button_size_group.add_widget(self.watermark_entry)
        watermark_hbox.pack_start(watermark_label, False, False, 12)
        watermark_hbox.pack_end(self.watermark_entry, False, False, 12)
        self.vbox.pack_start(watermark_hbox, False, False, 3)

	# Font Chooser
        font_chooser_hbox = Gtk.Box(spacing=3)
        font_chooser_label = Gtk.Label(label=_("Font chooser"))
        self.font_chooser_button = Gtk.Button(label=_("Select font"))
        self.font_chooser_button.connect("clicked", self.on_font_selected)
        button_size_group.add_widget(self.font_chooser_button)
        font_chooser_hbox.pack_start(font_chooser_label, False, False, 12)
        font_chooser_hbox.pack_end(self.font_chooser_button, False, False, 12)
        self.vbox.pack_start(font_chooser_hbox, False, False, 3)

        # Output path selection horizontal box
        output_hbox = Gtk.Box(spacing=3)
        output_label = Gtk.Label(label=_("Select Output Folder"))
        self.output_filechooser_button = Gtk.FileChooserButton()
        self.output_filechooser_button.set_title("Select Output Folder")
        self.output_filechooser_button.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.output_filechooser_button.set_current_folder(self.output_folder_path)
        button_size_group.add_widget(self.output_filechooser_button)
        output_hbox.pack_start(output_label, False, False, 12)
        output_hbox.pack_end(self.output_filechooser_button, False, False, 12)
        self.vbox.pack_start(output_hbox, False, False, 3)

        # Expert options section
        self.expert_options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        expert_title_label = Gtk.Label(label=_("Expert Options"))
        expert_title_label.set_markup("<b>{}</b>".format(_("Expert Options")))
        self.expert_options_box.pack_start(expert_title_label, False, False, 0)

        # Rotation angle
        rotation_hbox = Gtk.Box(spacing=3)
        rotation_label = Gtk.Label(label=_("Text Angle (degrees)"))
        # Create a Gtk.Scale widget for setting the rotation angle
        adjustment_rotation = Gtk.Adjustment(value=self.rotation_angle,
                                             lower=0, upper=90, step_increment=1, page_increment=4)
        self.rotation_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                        adjustment=adjustment_rotation)
        self.rotation_scale.set_digits(0)
        self.rotation_scale.connect("value-changed", self.on_rotation_angle_changed)
        button_size_group.add_widget(self.rotation_scale)
        rotation_hbox.pack_start(rotation_label, False, False, 12)
        rotation_hbox.pack_end(self.rotation_scale, False, False, 12)
        self.expert_options_box.pack_start(rotation_hbox, False, False, 3)

        # Font density
        density_hbox = Gtk.Box(spacing=3)
        density_label = Gtk.Label(label=_("Font Density"))
        adjustment_density = Gtk.Adjustment(value=self.fili_density, lower=1,
                                            upper=200, step_increment=1, page_increment=10)
        self.text_density_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                            adjustment=adjustment_density)
        self.text_density_scale.set_digits(0)
        self.text_density_scale.set_inverted(False)
        button_size_group.add_widget(self.text_density_scale)
        density_hbox.pack_start(density_label, False, False, 12)
        density_hbox.pack_end(self.text_density_scale, False, False, 12)
        self.expert_options_box.pack_start(density_hbox, False, False, 3)

        prefix_filename_hbox = Gtk.Box(spacing=6)
        prefix_filename_label = Gtk.Label(label=_("Filename Prefix"))
        self.watermark_prefix = Gtk.Entry()
        self.watermark_prefix.set_placeholder_text(_("Filename Prefix"))

        prefix_filename_hbox.pack_start(prefix_filename_label, False, False, 10)
        prefix_filename_hbox.pack_start(self.watermark_prefix, False, False, 10)
        self.expert_options_box.pack_start(prefix_filename_hbox, False, False, 3)

        date_filename_hbox = Gtk.Box(spacing=6)
        date_filename_label = Gtk.Label(label=_("Add Date + Hour in filename"))
        self.date_filename_check = Gtk.CheckButton()
        self.date_filename_check.set_active(True)
        date_filename_hbox.pack_start(date_filename_label, False, False, 10)
        date_filename_hbox.pack_start(self.date_filename_check, False, False, 10)
        self.expert_options_box.pack_start(date_filename_hbox, False, False, 3)

	# JPEG Compression level
        compression_rate_hbox = Gtk.Box(spacing=3)
        compression_rate_label = Gtk.Label(label=_("JPEG Compression"))
        adjustment_compression = Gtk.Adjustment(value=self.compression_rate,
                                                lower=0, upper=100, step_increment=1,
                                                page_increment=10)
        self.compression_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                           adjustment=adjustment_compression)
        self.compression_scale.set_digits(0)
        self.compression_scale.connect("value-changed", self.on_compression_changed)
        button_size_group.add_widget(self.compression_scale)
        compression_rate_hbox.pack_start(compression_rate_label, False, False, 12)
        compression_rate_hbox.pack_end(self.compression_scale, False, False, 12)
        self.expert_options_box.pack_start(compression_rate_hbox, False, False, 3)

        #self.vbox.pack_start(self.expert_options_box, False, False, 12)
        #self.expert_options_box.hide()

        # Add watermark button horizontal box
        self.watermarkb_hbox = Gtk.Box(spacing=3)
        add_watermark_button = Gtk.Button(label=_("Add Watermark"))
        add_watermark_button.connect("clicked", self.on_add_watermark_clicked)
        self.watermarkb_hbox.pack_start(add_watermark_button, False, False, 12)
        self.vbox.pack_start(self.watermarkb_hbox, False, False, 3)


    def on_font_selected(self, widget):
        dialog = Gtk.FontChooserDialog(title="Choose a Font", transient_for=self, flags=0)
        #default_font_description = Pango.FontDescription("Sans 20")

        while True:
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                font_desc = dialog.get_font()
                print(font_desc)
                #font_description = Pango.FontDescription.from_string(font_desc)
                font_path = self.find_font_file(font_desc)

                if font_path:
                    self.font_base_name = font_path.split('.ttf')[0] + '.ttf'
                    print(f"Font name: {self.font_base_name}")
                    parts_desc = font_desc.split()
                    self.font_size = int(parts_desc[-1]) if parts_desc else None
                    self.font_chooser_button.set_label(font_desc)
                    dialog.destroy()
                    return self.font_base_name, self.font_size
                else:
                    print("Could not find the font file.")
                    warning_dialog = WarningDialog(
                        title="Error",
                        message=_("An error occurred, can't find the font path, please choose another one"),
                    )
                    warning_dialog.show()

            elif response == Gtk.ResponseType.CANCEL:
                print("Select font canceled.")
                dialog.destroy()
                return None

    def find_font_file(self, font_description):
        """
        Try to find the font file for a given Pango font description.
        Uses `fc-list` command line tool from fontconfig package.
        """
        try:
            # Use fc-list to get all installed fonts and filter by family name
            result = subprocess.run(
                ['fc-list', ':family:' + font_description.split()[0]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=True
            )

            # Extract the file path from the output
            for line in result.stdout.splitlines():
                if font_description.split()[0] in line and '.ttf' in line:
                    return line

            return None
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def on_rotation_angle_changed(self, widget):
        self.rotation_angle = int(widget.get_value())

    def on_rotation_density_changed(self, widget):
        self.fili_density = int(widget.get_value())

    def on_compression_changed(self, widget):
        self.compression_rate = int(widget.get_value())

    def on_expert_toggle(self, checkmenuitem):
        if self.expert_options_check.get_active():
            self.vbox.remove(self.watermarkb_hbox)
            self.vbox.pack_start(self.expert_options_box, False, False, 12)
            self.vbox.pack_start(self.watermarkb_hbox, False, False, 3)
            self.expert_options_box.show_all()
        else:
            if self.expert_options_box.get_parent() is not None:
                self.expert_options_box.hide()
                #self.vbox.pack_start(self.watermarkb_hbox, False, False, 3)
                self.vbox.remove(self.expert_options_box)
                self.resize(210, 110)

    def about_dialog(self, widget):
        # Create a custom dialog window for the About section with a clickable link
        about_window = Gtk.Window(title=_("About Watermark App"))
        about_window.set_default_size(400, 250)
        about_window.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        about_window.add(vbox)

        info_text = _(
            "Watermark App Version 3.0\n\n"
            "This app add a Watermark to images\n"
            "Licence GPL2 \n\n"
            "Open Source Project on GitHub: "
        )

        label = Gtk.Label(label=info_text)
        vbox.pack_start(label, True, True, 12)

        # Create a clickable hyperlink using GtkLinkButton
        github_link = Gtk.LinkButton("https://github.com/aginies/watermark",
                                     "https://github.com/aginies/watermark")
        vbox.pack_start(github_link, False, False, 12)

        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", lambda btn: about_window.destroy())
        vbox.pack_end(close_button, False, False, 12)

        # Show the window and all its children
        about_window.show_all()

    def main_display_images(self, image_path):
        app = ImageViewerWindow()
        app.load_images(image_path)

    def add_images_filters(self):
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Image Files")
        filter_img.add_mime_type("text/plain")
        filter_img.add_mime_type("image/png")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_mime_type("image/gif")
        filter_img.add_mime_type("image/bmp")
        filter_img.add_mime_type("image/tiff")
        filter_img.add_pattern("*.png")
        filter_img.add_pattern("*.jpg")
        filter_img.add_pattern("*.jpeg")
        filter_img.add_pattern("*.gif")
        filter_img.add_pattern("*.bmp")
        filter_img.add_pattern("*.tiff")
        filter_img.add_pattern("*.tif")
        return filter_img

    def on_files_clicked(self, widget):
        # Create a file chooser dialog with multiple selection option
        dialog = Gtk.FileChooserDialog(
            _("Please choose files"),
            self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )

        # Set the dialog to allow multiple selections
        dialog.set_select_multiple(True)

        # Add filters
        image_filter = self.add_images_filters()
        print(f"Filter name: {image_filter.get_name()}")
        dialog.add_filter(image_filter)
        dialog.set_filter(image_filter)
        filters = dialog.list_filters()
        for lfil, fil in enumerate(filters):
            print(f"Listed Filter {lfil}: {fil.get_name()}")

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            file_paths = dialog.get_files()
            self.selected_files_path = [file.get_path() for file in file_paths]
            self.update_file_button_text()
            print("Selected files:", self.selected_files_path)
            self.files_selected_hbox.show()
            for file in file_paths:
                print(file.get_path())

        dialog.destroy()

    def update_file_button_text(self):
        selected_files_str = "\n".join(os.path.basename(path) for path in self.selected_files_path)
        self.files_label.set_text(_(f"Selected File(s):\n{selected_files_str}"))

    def on_file_selected(self, widget):
        file_paths = widget.get_filenames()
        if file_paths:
            self.selected_files_path.extend(file_paths)
            print("Selected files:", self.selected_files_path)

    def on_folder_selected(self, widget):
        folder_path = widget.get_filename()
        if folder_path:
            self.output_folder_path = folder_path
            print("Output folder selected:", self.output_folder_path)
            self.output_filechooser_button.set_current_folder(self.output_folder_path)

    def on_add_watermark_clicked(self, widget):
        if not self.selected_files_path:
            warning_dialog = WarningDialog(
                title="Warning",
                message=_("Please select an image."),
            )
            warning_dialog.show()
            return

        watermark_text = self.watermark_entry.get_text()
        if not watermark_text:
            warning_dialog = WarningDialog(
                title="Warning",
                message=_("Please enter a watermark text."),
            )
            warning_dialog.show()
            return

        if self.font_base_name is None:
            warning_dialog = WarningDialog(
                title="Warning",
                message=_("Please Select a Font"),
            )
            warning_dialog.show()
            return

        if not self.output_folder_path:
            default_output_dir = os.path.dirname(self.selected_files_path[0])
            self.output_filechooser_button.set_current_folder(default_output_dir)
        else:
            default_output_dir = self.output_folder_path
            self.output_filechooser_button.set_current_folder(self.output_folder_path)

        try:
            for image_path in self.selected_files_path:
                output_image_path = self.add_watermark_to_image(image_path, watermark_text)
                if output_image_path:
                    print("Success", f"Generated File: {os.path.basename(output_image_path)}\n")
                    self.all_images.append(output_image_path)

            self.main_display_images(self.all_images)
            self.all_images = []

        except Exception as err:
            print(f"Error processing the image: {err}")
            warning_dialog = WarningDialog(
                title="Error",
                message=_(f"An error occurred during image processing: {err}"),
            )
            warning_dialog.show()

    def get_current_time_ces(self):
        now = time.time()
        cest_time = time.localtime(now + 3600)
        return cest_time

    def add_watermark_to_image(self, image_path, text):
        try:
            with Image.open(image_path).convert("RGBA") as img:
                # Resize image if it's too large while preserving aspect ratio
                width_percent = (1280 / float(img.width))
                height_size = int((float(img.height) * float(width_percent)))

                if max(img.size) > 1280:
                    img = img.resize((1280, height_size), Image.LANCZOS)

                draw = ImageDraw.Draw(img)
                cest_time = self.get_current_time_ces()
                font = ImageFont.truetype(self.font_base_name, int(self.font_size))

                timestamp_str_text = time.strftime('%d%m%Y_%H%M%S', cest_time)
                full_watermark_text = f"{text} {timestamp_str_text}"
                bbox = draw.textbbox((0, 0), full_watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                dpi_from_box = int(self.text_density_scale.get_value())
                dpi = 201 - dpi_from_box
                interval_pixels_y = int(dpi)
                used_positions = set()

                # Draw the continuous watermark across the image
                for ydata in range(interval_pixels_y, img.height, interval_pixels_y):
                    x_positions = [(xdata % img.width) for xdata in range(0, img.width, text_width)]

                    for xdata in x_positions:
                        if (xdata, ydata) not in used_positions:
                            angle = random.uniform(- int(self.rotation_scale.get_value()),
                                                   int(self.rotation_scale.get_value()))
                            color = (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255),
                                50 # Adjust transparency
                            )
                            rotated_text_img = Image.new('RGBA', img.size)
                            ImageDraw.Draw(rotated_text_img)
                            temp_image = Image.new('RGBA', (text_width * 3,
                                                            text_height * 3), (0, 0, 0, 0))
                            temp_draw = ImageDraw.Draw(temp_image)
                            temp_draw.text((text_width, text_height),
                                           full_watermark_text, font=font, fill=color)
                            rotated_text = temp_image.rotate(angle, expand=True)
                            rotated_text_position = (
                                xdata + text_width / 2 - rotated_text.width / 2,
                                ydata + text_height / 2 - rotated_text.height / 2
                            )
                            img.paste(rotated_text, (int(rotated_text_position[0]),
                                                     int(rotated_text_position[1])),
                                      mask=rotated_text)
                            used_positions.add((xdata, ydata))

                timestamp_str = time.strftime('%d%m%Y_%H%M%S', cest_time)
                original_filename = os.path.basename(image_path)
                name_without_ext = os.path.splitext(original_filename)[0]
                fprefix = ""
                if self.watermark_prefix.get_text() != "":
                    fprefix = self.watermark_prefix.get_text() + "_"
                if self.date_filename_check.get_active():
                    final_filename = f"{fprefix}{text}_{timestamp_str}_{name_without_ext}.jpg"
                else:
                    final_filename = f"{fprefix}{text}_{name_without_ext}.jpg"

                output_path = os.path.join(self.output_folder_path, final_filename)
                img.convert("RGB").save(output_path, "JPEG", quality=self.compression_rate)
                return output_path

        except Exception as err:
            print(f"Error adding watermark: {err}")
            warning_dialog = WarningDialog(
                title="Error",
                message=_(f"An error occurred while adding the watermark: {err}"),
            )
            warning_dialog.show()
            return None

WIN = WatermarkApp()
WIN.connect("destroy", Gtk.main_quit)
WIN.show_all()
# Hide expert option per default
WIN.expert_options_box.hide()
WIN.files_selected_hbox.hide()
Gtk.main()
