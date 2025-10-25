import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
import os
import math

def scale_ascii(ascii_text, scale=0.5):
    """Scale ASCII text by any ratio between 0 and 1."""
    lines = ascii_text.splitlines()
    if not lines:
        return ""

    original_height = len(lines)
    original_width = max(len(line) for line in lines)
    new_height = max(int(original_height * scale), 1)
    new_width = max(int(original_width * scale), 1)

    scaled_lines = []
    for i in range(new_height):
        # map new line index to original line index
        orig_i = int(i / scale)
        orig_i = min(orig_i, original_height - 1)
        line = lines[orig_i]
        new_line = ""
        for j in range(new_width):
            orig_j = int(j / scale)
            orig_j = min(orig_j, len(line) - 1)
            new_line += line[orig_j]
        scaled_lines.append(new_line)
    return "\n".join(scaled_lines)

def process_file():
    file_path = filedialog.askopenfilename(
        title="Select ASCII text file or image",
        filetypes=[("Text or Image files", "*.txt *.png *.jpg *.jpeg"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".png", ".jpg", ".jpeg"]:
            img = Image.open(file_path)
            ascii_text = pytesseract.image_to_string(img, config="--psm 6")
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                ascii_text = f.read()
        else:
            messagebox.showerror("Error", "Unsupported file type.")
            return

        scale_value = scale_slider.get() / 100  # convert slider % to 0-1
        scaled_ascii = scale_ascii(ascii_text, scale_value)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save scaled ASCII art"
        )
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(scaled_ascii)
            messagebox.showinfo("Success", f"Saved scaled ASCII art to:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# --- GUI ---
root = tk.Tk()
root.title("ASCII Art Scaler")
root.geometry("450x250")

label = tk.Label(root, text="Scale ASCII Art", font=("Arial", 14))
label.pack(pady=10)

scale_slider = tk.Scale(root, from_=25, to=100, orient=tk.HORIZONTAL, length=300,
                        label="Scale (%)", font=("Arial", 12))
scale_slider.set(50)  # default 50%
scale_slider.pack(pady=10)

button = tk.Button(root, text="Upload Image or Text File", command=process_file, font=("Arial", 12))
button.pack(pady=20)

root.mainloop()
