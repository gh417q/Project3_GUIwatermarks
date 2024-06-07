import tkinter
from tkinter import Tk, Label, Button, filedialog, DISABLED, NORMAL, CENTER, StringVar, Radiobutton
from PIL import ImageTk, Image
import os

IMG_HEIGHT = 800
IMG_WIDTH = 1200
PAD_X = 20
PAD_Y = 70
WATERMARKS_DIR = "watermarks"
WATERMARKS = ["Copyright_watermark-25.png", "Copyright_watermark-30.png", "Copyright_watermark-35.png"]

image_to_process = None
image_to_save = None
watermarks = {}


# Initial load of available watermarks
def load_watermarks():
    for image in WATERMARKS:
        watermark_image = Image.open(f"{WATERMARKS_DIR}/{image}")
        watermark_image = watermark_image.convert("RGBA")
        watermarks[image] = watermark_image


# Change state of watermark radio buttons. Should be disabled when no image is loaded
def watermark_group_state(group_state: int):
    radio_none.config(state=group_state)
    radio_25.config(state=group_state)
    radio_30.config(state=group_state)
    radio_35.config(state=group_state)


# Display the image, loaded or with applied watermarks. Use copy as it may be resized if it's too big.
def show_image(image: Image):
    sample = image.copy()  # keep the original unchanged if resize is needed right below
    sample.thumbnail((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(sample)
    lbl_image.config(image=img)
    lbl_image.image = img  # to keep the img reference and avoid garbage collecting on function exit


# Opens new file
def open_image_file():
    global image_to_process
    file_path = filedialog.askopenfilename(title="Select Image",
                                           filetypes=[("All images", "*.bmp;*.jpg;*.jpeg;*.gif;*.png"),
                                                      ("Bitmap files", "*.bmp"), ("JPEG", "*.jpg;*.jpeg"),
                                                      ("GIF", "*.gif"), ("PNG", "*.png")])
    if file_path:
        image_to_process = Image.open(file_path)
        show_image(image=image_to_process)
        lbl_image_name.config(text=f"Selected Image: {file_path}")
        btn_open.config(text="Open another image")
        watermark_group_state(group_state=NORMAL)
        radio_none.select()
        btn_save.config(state=DISABLED)


# Applies selected watermark oor displays original image if "No watermark" is selected.
def select_watermark():
    global image_to_save
    if image_to_process is None:
        return
    if var_watermark.get() == "None":
        show_image(image=image_to_process)
        btn_save.config(state=DISABLED)
        return
    watermark_to_apply = watermarks[var_watermark.get()]  # already RGBA
    image_to_save = image_to_process.convert("RGBA")
    for m in range(100, image_to_save.size[1], 200):
        for k in range(100 - (m + 100)%400, image_to_save.size[0], 400):
            image_to_save.paste(watermark_to_apply, (k, m), mask=watermark_to_apply)
    show_image(image=image_to_save)
    btn_save.config(state=NORMAL)


# Saves processed image.
def save_image():
    if image_to_save is None:
        return
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=[("PNG file", "*.png")])
    if file:
        full_path = os.path.abspath(file.name)
        image_to_save.save(full_path)


window = Tk()
window.title("Image Processing")
window.geometry(f"{IMG_WIDTH + PAD_X*2}x{IMG_HEIGHT + PAD_Y*2}")
window.grid_rowconfigure(0, minsize=IMG_HEIGHT)

lbl_image = Label(window, text="Select an image")  #, bg="#60c060")  #, width=IMG_WIDTH)
lbl_image.grid(row=0, column=0, columnspan=5)

lbl_image_name = Label(window, width=175, text="No image selected", justify=CENTER)  #, bg="#f7f5dd")
lbl_image_name.grid(row=1, column=1, columnspan=3)

btn_open = Button(window, text="Open image", highlightthickness=1, command=open_image_file)
btn_open.grid(row=2, column=1)

btn_save = Button(window, text="Save Processed Image", highlightthickness=1, command=save_image, state=DISABLED)
btn_save.grid(row=2, column=3)

var_watermark = StringVar(value="None")

radio_none = Radiobutton(window, text="No Watermark", variable=var_watermark, value="None", command=select_watermark)
radio_none.grid(row=2, column=2)
radio_25 = Radiobutton(window, text="Copyright-25", variable=var_watermark,
                       value="Copyright_watermark-25.png", command=select_watermark)
radio_25.grid(row=3, column=2)
radio_30 = Radiobutton(window, text="Copyright-30", variable=var_watermark,
                       value="Copyright_watermark-30.png", command=select_watermark)
radio_30.grid(row=4, column=2)
radio_35 = Radiobutton(window, text="Copyright-35", variable=var_watermark,
                       value="Copyright_watermark-35.png", command=select_watermark)
radio_35.grid(row=5, column=2)

watermark_group_state(group_state=DISABLED)

load_watermarks()

open_image_file()

window.mainloop()
