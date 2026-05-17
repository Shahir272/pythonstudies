import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter  # Added ImageFilter here

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python RGB Master Editor")
        self.orig = None  
        self.display = None

        # --- Step 1: UI Layout ---
        tk.Button(root, text="Step 1s-: Upload Image", command=self.upload, bg="lightgrey").pack(pady=5)
        
        self.label = tk.Label(root)
        self.label.pack()

        # Sliders for different effects
        self.contrast = tk.Scale(root, from_=0.5, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, 
                                 label="Contrast Factor", length=400, command=self.update)
        self.contrast.set(1.0)
        self.contrast.pack()

        self.grayscale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, 
                                  label="Grayscale Intensity %", length=400, command=self.update)
        self.grayscale.pack()

        self.blur = tk.Scale(root, from_=0, to=5, orient=tk.HORIZONTAL, 
                             label="Blur Radius (0-5)", length=400, command=self.update)
        self.blur.pack()

        # Step 3: Save Button
        tk.Button(root, text="Step 3: Save Result", bg="lightblue", 
                  command=self.save_image).pack(pady=10)

    def upload(self):
        fpath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if fpath:
            img = Image.open(fpath).convert("RGB")
            # Resize to fit screen (Lambert style constraint)
            img.thumbnail((800, 600), Image.Resampling.LANCZOS)
            self.orig = img
            self.update(None)

    def update(self, _):
        if not self.orig: return 
        
        c_fac = float(self.contrast.get())
        g_fac = self.grayscale.get() / 100.0
        b_rad = int(self.blur.get())
        
        # 1. Apply Blurring (Spatial filtering)
        if b_rad > 0:
            # Using the correctly imported ImageFilter module
            img = self.orig.filter(ImageFilter.BoxBlur(b_rad))
        else:
            img = self.orig.copy()
            
        pix = img.load()

        # 2. Pixel Loop for Contrast and Grayscale (Point processing)
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pix[x, y]

                # Contrast Math: (Pixel - 128) * factor + 128
                r = int((r - 128) * c_fac + 128)
                g = int((g - 128) * c_fac + 128)
                b = int((b - 128) * c_fac + 128)

                # Grayscale Math (Luminance weights)
                gray = int(r * 0.299 + g * 0.587 + b * 0.114)
                
                # Blend color with gray based on slider intensity
                r = int(r * (1 - g_fac) + gray * g_fac)
                g = int(g * (1 - g_fac) + gray * g_fac)
                b = int(b * (1 - g_fac) + gray * g_fac)

                # Clamp to [0, 255] to prevent RGB overflow
                pix[x, y] = (max(0, min(255, r)), 
                             max(0, min(255, g)), 
                             max(0, min(255, b)))

        self.display = img
        self.refresh_display()

    def refresh_display(self):
        """ Updates the image in the Tkinter window """
        tk_img = ImageTk.PhotoImage(self.display)
        self.label.config(image=tk_img)
        self.label.image = tk_img 

    def save_image(self):
        if self.display:
            self.display.save("edited_output.png")
            print("Successfully saved to edited_output.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoEditor(root)
    root.mainloop()
