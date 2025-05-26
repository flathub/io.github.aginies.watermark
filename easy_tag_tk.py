#!/usr/bin/python3
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
        self.root.title("Ajout Filigrane Image")
        self.selected_file_path = ""
        self.output_folder_path = ""

        # File selection label and button
        tk.Label(root, text="Selection Image:").grid(row=0, column=0, padx=10, pady=5)
        self.file_button = tk.Button(root, text="Select a File", command=self.select_file)
        self.file_button.grid(row=0, column=1, padx=10, pady=5)

        # Filigrane text label and entry
        tk.Label(root, text="Filigrane Text:").grid(row=1, column=0, padx=10, pady=5)
        self.filigrane_entry = tk.Entry(root)
        self.filigrane_entry.insert(0, "FILIGRANE A AJOUTER")
        self.filigrane_entry.grid(row=1, column=1, padx=10, pady=5)

        # Output path selection label and button
        tk.Label(root, text="Répertoire Sauvegarde:").grid(row=2, column=0, padx=10, pady=5)
        self.output_button = tk.Button(root, text="Select Output Folder", command=self.select_output_folder)
        self.output_button.grid(row=2, column=1, padx=10, pady=5)

        # Add filigrane button
        self.add_filigrane_button = tk.Button(root, text="Génération Image", command=self.on_add_filigrane_clicked)
        self.add_filigrane_button.grid(row=3, columnspan=2, pady=10)

        # Image display label
        self.image_label = tk.Label(root)
        self.image_label.grid(row=4, columnspan=2, pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            self.file_button.config(text=os.path.basename(file_path))
            self.selected_file_path = file_path

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_button.config(text=os.path.basename(folder_path))
            self.output_folder_path = folder_path

    def on_add_filigrane_clicked(self):
        # Check if a file is selected
        if not self.selected_file_path:
            messagebox.showwarning("Input Error", "Please select an image file first")
            return

        filigrane_text = self.filigrane_entry.get()

        if not filigrane_text:
            messagebox.showwarning("Input Error", "Please enter filigrane text")
            return

        # Check if output folder is selected
        if not self.output_folder_path:
            messagebox.showwarning("Input Error", "Please select an output folder")
            return

        try:
            # Call the function to add filigrane and get output image path
            output_image_path = self.add_filigrane_to_image(self.selected_file_path, filigrane_text)

            if output_image_path and os.path.exists(output_image_path):
                img = Image.open(output_image_path)
                img.thumbnail((400, 400))  # Resize for display
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep a reference to avoid garbage collection
            else:
                messagebox.showerror("Generation Error", "Failed to generate image with filigrane!")

        except Exception as err:
            print(f"Error processing the image: {err}")
            messagebox.showerror("Processing Error", f"An error occurred while processing the image: {err}")

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
                #text_width, text_height = draw.textsize(full_filigrane_text, font=font)
                # Use textbbox to get the bounding box of the text
                bbox = draw.textbbox((0, 0), full_filigrane_text, font=font)

                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

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
            output_path = os.path.join(self.output_folder_path, final_filename)
            img.convert("RGB").save(output_path, "JPEG", quality=75)
            return output_path

        except Exception as err:
            print(f"Error adding filigrane: {err}")
            messagebox.showerror("Filigrane Error", f"An error occurred while adding the filigrane: {err}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = FiligraneApp(root)
    root.mainloop()

