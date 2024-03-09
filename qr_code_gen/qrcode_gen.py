import tkinter as tk
from PIL import Image, ImageTk
import pyqrcode
import pyperclip
import atexit
import os

class App(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.text_label = tk.Label(text="Enter the text to be encoded:")
        self.text_label.grid(row=0, column=0)
        self.text_entry = tk.Entry()
        self.text_entry.grid(row=0, column=1)
        generate_button = tk.Button(text="Generate QR Code", command=self.generate_from_entry)
        generate_button.grid(row=1, column=0)
        generate_button2 = tk.Button(text="Paste and Generate", command=self.paste_and_generate)
        generate_button2.grid(row=1, column=1)
        self.image_path = 'qr_code.png'
        atexit.register(self.delete_file)

    def generate_from_entry(self):
        text = self.text_entry.get()
        if not text:
            self.text_entry.insert(tk.END, pyperclip.paste()) 
            text = self.text_entry.get()
        self.generate_qrcode(text)
   
    def paste_and_generate(self):    
        self.text_entry.delete(0, tk.END) # Clear the entry field
        self.text_entry.insert(tk.END, pyperclip.paste()) 
        text = self.text_entry.get()
        self.generate_qrcode(text)

    def generate_qrcode(self, text):
        qr = pyqrcode.create(text) 
        qr.png(self.image_path)
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((self.image.width * 10, self.image.height * 10))  # zoom half
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        self.canvas.grid(row=2, column=0, columnspan=2)
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

    def delete_file(self):
        if os.path.isfile(self.image_path):
            os.remove(self.image_path)


app = App()
app.title("QR Code Generator")
app.mainloop()
