#!/usr/bin/python3
# antoine@ginies.org
# GPL2

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import tempfile
import random
import time

class FiligraneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filigrane App Image")
        self.root.resizable(False, False)
        self.output_folder_path = ""
        self.selected_file_path = ""
        self.compression_rate = 75
        self.fili_font_size = 20
        self.fili_density = 12

        # Main frame for all widgets
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure row and column weights to make the layout responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Quit", command=self.root.quit)
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="A Propos", menu=about_menu)
        about_menu.add_command(label="A Propos de Filigrane App", command=self.about_dialog)

        # File selection frame
        file_frame = tk.Frame(main_frame)
        file_frame.grid(row=0, column=0, pady=5, sticky="ew")
        tk.Label(file_frame, text="Sélection Image").pack(side="left", padx=(0, 10))
        self.file_button = tk.Button(file_frame, text="Sélection", command=self.select_file)
        self.file_button.pack(side="right")

        # Filigrane text frame
        filigrane_frame = tk.Frame(main_frame)
        filigrane_frame.grid(row=1, column=0, pady=5, sticky="ew")
        tk.Label(filigrane_frame, text="Filigrane Texte").pack(side="left", padx=(0, 10))
        self.filigrane_entry = tk.Entry(filigrane_frame)
        self.filigrane_entry.insert(0, "Filigrane à Ajouter")
        self.filigrane_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        tk.Label(filigrane_frame, text="+ Date_Heure").pack(side="right")

        # Output path selection frame
        output_frame = tk.Frame(main_frame)
        output_frame.grid(row=2, column=0, pady=5, sticky="ew")
        tk.Label(output_frame, text="Répertoire Sauvegarde").pack(side="left", padx=(0, 10))
        self.output_button = tk.Button(output_frame, text="Sélection", command=self.select_output_folder)
        self.output_button.pack(side="right")

        # Expert mode toggle
        self.expert_mode_var = tk.BooleanVar(value=False)
        self.expert_mode_checkbox = tk.Checkbutton(main_frame, text="Expert Mode", variable=self.expert_mode_var, command=self.toggle_expert_mode)
        #self.expert_mode_checkbox.grid(row=3, column=0, pady=(10, 5), sticky='w')

        # Add filigrane button
        self.add_filigrane_button = tk.Button(main_frame, text="Génération Image", command=self.on_add_filigrane_clicked)
        self.add_filigrane_button.grid(row=4, column=0, pady=(10, 5))

        # Generated file label
        self.generated_file_label = tk.Label(main_frame, text="")
        self.generated_file_label.grid(row=5, column=0, pady=5)

        # Image display label
        self.image_label = tk.Label(main_frame)
        self.image_label.grid(row=6, column=0, pady=(5, 10))
        
    def select_file(self):
    # Specify the file types for the dialog
        filetypes = [
            ("All files", "*.*"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
        ]

        file_path = filedialog.askopenfilename(title="Sélection d'un fichier", filetypes=filetypes)
        if file_path:
            self.file_button.config(text=os.path.basename(file_path))
            self.selected_file_path = file_path

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_button.config(text=os.path.basename(folder_path))
            self.output_folder_path = folder_path

    def toggle_expert_mode(self):
        """Show or hide the expert mode settings."""
        if self.expert_mode_var.get():
            self.show_expert_settings()
        else:
            self.hide_expert_settings()

    def show_expert_settings(self):
        """Display the additional settings for expert mode."""
        # Compression rate
        tk.Label(self.root, text="Compression du JPEG (0=aucune; 95=Forte)").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.compression_entry = tk.Entry(self.root)
        self.compression_entry.insert(0, str(self.compression_rate))
        self.compression_entry.grid(row=5, column=1, padx=10, pady=5)

        # Fili Density
        #tk.Label(self.root, text="Densité (5-20):").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        #self.density_entry = tk.Entry(self.root)
        #self.density_entry.insert(0, str(self.fili_density))
        #self.density_entry.grid(row=6, column=1, padx=10, pady=5)

    def hide_expert_settings(self):
        """Hide the additional settings for expert mode."""
        # Destroy labels and entries to hide them
        try:
            # Compression rate label and entry
            self.root.grid_slaves(row=5, column=0)[0].destroy()
            self.compression_entry.destroy()
            #self.root.grid_slaves(row=6, column=0)[0].destroy()
            #self.density_entry.destroy()
        except (IndexError, AttributeError):
            pass

    def about_dialog(self):
        # Create a custom dialog window for the About section with a clickable link
        about_window = tk.Toplevel(self.root)
        about_window.title("About Filigrane App")
        about_window.resizable(False, False)
        info_text = (
            "Filigrane App Version 1.1\n\n"
            "Cette application ajoute un filigrane à une image\n"
            "Licence GPL2 \n\n"
            "Project Open Source sur GitHub: "
        )

        label = tk.Label(about_window, text=info_text)
        label.pack(padx=20, pady=10)

        # Create a clickable hyperlink
        github_link = tk.Label(about_window, text="https://github.com/aginies/easy_tag", foreground="blue", cursor="hand2")
        github_link.pack(padx=20, pady=5)
        github_link.bind("<Button-1>", lambda e: self.open_github())

        close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
        close_button.pack(pady=10)

    def open_github(self):
        # Open the GitHub link in the default web browser
        import webbrowser
        webbrowser.open("https://github.com/aginies/easy_tag")

    def on_add_filigrane_clicked(self):
        # Check if a file is selected
        if not self.selected_file_path:
            messagebox.showwarning("Input Error", "SVP Séléctionnez une image")
            return

        filigrane_text = self.filigrane_entry.get()

        if not filigrane_text:
            messagebox.showwarning("Input Error", "SVP Entrez un texte pour le filigrane")
            return

        if not self.output_folder_path:
            default_output_dir = os.path.dirname(self.selected_file_path)
        else:
            default_output_dir = self.output_folder_path
            
        try:
            # Call the function to add filigrane and get output image path
            output_image_path = self.add_filigrane_to_image(self.selected_file_path, filigrane_text)
            if output_image_path:
            # Load the output image for display in Tkinter
                img = Image.open(output_image_path)
                img.thumbnail((800, 600), Image.LANCZOS)
                self.tk_img = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.tk_img)
                self.generated_file_label.config(text=f"Generated File: {os.path.basename(output_image_path)}")
                
        except Exception as err:
            print(f"Error processing the image: {err}")
            messagebox.showerror("Processing Error", f"Une erreur lors du traitement de l'image: {err}")

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
                img = img.resize((1280, height_size), Image.LANCZOS)

            draw = ImageDraw.Draw(img)

            cest_time = self.get_current_time_ces()

            if os.path.exists('/usr/share/fonts/truetype/DejaVuSans.ttf'):
                font = ImageFont.truetype("DejaVuSans.ttf", self.fili_font_size)
            else:
                print("Pas trouvé de Font DejaVuSans....")
                font = ImageFont.load_default()

            timestamp_str_text = time.strftime('%d%m%Y_%H%M%S', cest_time)
            full_filigrane_text = f"{text} {timestamp_str_text}"
            bbox = draw.textbbox((0, 0), full_filigrane_text, font=font)

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            dpi = self.fili_density
            interval_pixels = int(1 * dpi)
            
            for y in range(interval_pixels, img.height, interval_pixels):
                if y < text_height:
                    x_positions = [random.randint(max(0, img.width // 2 - text_width), min(img.width // 2 + text_width, img.width))]
                elif y > img.height - text_height:
                    x_positions = [random.randint(0, min(img.width - text_width, text_width))]
                else:
                    left_x_end = max(0, (img.width // 3) - text_width)
                    right_x_start = img.width - (img.width // 3)

                    if left_x_end < 0 and right_x_start >= img.width:
                        x_positions = []
                    elif left_x_end < 0:
                        x_positions = [random.randint(right_x_start, min(img.width, right_x_start + text_width))]
                    elif right_x_start >= img.width:
                        x_positions = [random.randint(left_x_end, min(img.width // 3, img.width))]
                    else:
                        x_positions = [
                            random.randint(max(0, left_x_end), min(img.width // 3, img.width)),
                            random.randint(right_x_start, min(img.width, right_x_start + text_width))
                        ]
            
                for x in x_positions:
                    angle = random.uniform(-30, 40)

                    color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                        40
                    )

                    rotated_text_img = Image.new('RGBA', img.size)
                    draw_rotated = ImageDraw.Draw(rotated_text_img)

                    text_position = (x + text_width, y + text_height / 2)
                    temp_image = Image.new('RGBA', (text_width * 3, text_height * 3), (0, 0, 0, 0))
                    temp_draw = ImageDraw.Draw(temp_image)
                    temp_draw.text((text_width, text_height), full_filigrane_text, font=font, fill=color)

                    rotated_text = temp_image.rotate(angle, expand=True)

                    rotated_text_position = (
                        x + text_width / 2 - rotated_text.width / 2,
                        y + text_height / 2 - rotated_text.height / 2
                    )

                    img.paste(rotated_text, (int(rotated_text_position[0]), int(rotated_text_position[1])), mask=rotated_text)

            timestamp_str = time.strftime('%d%m%Y_%H%M%S', cest_time)
            original_filename = os.path.basename(image_path)
            name_without_ext = os.path.splitext(original_filename)[0]
            final_filename = f"ready_{text}_{timestamp_str}_{name_without_ext}.jpg"
            output_path = os.path.join(self.output_folder_path, final_filename)
            img.convert("RGB").save(output_path, "JPEG", quality=self.compression_rate)
            return output_path
            
        except Exception as err:
            print(f"Error adding filigrane: {err}")
            messagebox.showerror("Filigrane Error", f"An error occurred while adding the filigrane: {err}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = FiligraneApp(root)
    root.mainloop()
