from tkinter.filedialog import askopenfilename
from PIL import Image
from os import path
from tkinter import Button, Canvas, Entry, Label, Radiobutton, StringVar, Tk, messagebox
import random
import string
from typing import List, Tuple
from PIL import GifImagePlugin, ImageDraw, ImageFont

OFFSET = 10 # Pixel offset from edges to text
FONTS = {
    "small": ImageFont.truetype("comic.ttf", 12),
    "medium": ImageFont.truetype("comic.ttf", 24),
    "large": ImageFont.truetype("comic.ttf", 48)
}

"""
Saves the provided list of PIL Image objects as a GIF
"""
def save_gif(images: List[Image.Image], filepath, frame_duration):
    try:
        images[0].save(filepath, save_all=True, append_images=images[1:], optimize=True, duration=frame_duration, loop=0)
    except:
        exit()

"""
Puts the provided image on a white background of the provided size
"""
def white_bg(image: Image.Image, text: str, font_type: str):

    width = image.size[0]
    height = caption_area_height(image, text, font_type)

    background = Image.new("RGBA", (width, image.size[1]+height), (255, 255, 255, 255))
    background.paste(image, (0, height))
    
    return background


"""
Adds the caption to an image already on a white background of the right size
"""
def add_caption(image: Image, text: str, font_type: str):
    drawable = ImageDraw.Draw(image)
    y_coord = 0
    lines = text_splitting(image, text, font_type)
    line_height = FONTS[font_type].getsize(text)[1]
    for line in lines:
        drawable.text((OFFSET, y_coord), line, fill=(0, 0, 0, 255), font=FONTS[font_type])
        y_coord += line_height

    return image

"""
Computes the necessary height for the caption area
"""
def caption_area_height(image: Image.Image, text: str, font_type: str) -> int:

    image_size = image.size
    font = FONTS[font_type]
    font_size = font.getsize(text)


    if font_size[0] + 2*OFFSET <= image_size[0]: # Fits in one line
        return font_size[1] + OFFSET
    else:
        lines = len(text_splitting(image, text, font_type))
        return font_size[1]*lines + OFFSET

"""
Splits the caption in several lines fitting within the image width
"""
def text_splitting(image: Image.Image, text: str, font_type: str):
    
    image_size = image.size
    font = FONTS[font_type]
    font_size = font.getsize(text)

    if font_size[0] + 2*OFFSET <= image_size[0]:
        return [text]

    lines = []
    words_list = text.split(" ")

    while font.getsize(" ".join(words_list))[0] + 2*OFFSET > image_size[0]:
        pointer = 1
        while font.getsize(" ".join(words_list[:pointer]))[0] + 2*OFFSET <= image_size[0]:
            pointer += 1
        pointer -= 1
        lines.append(" ".join(words_list[:pointer]))
        words_list = words_list[pointer:]

    lines.append(" ".join(words_list))

    return lines


"""
Converts a GIF into a sequence of PNG images
"""
def GIF_to_sequence(filepath: str) -> Tuple[List[Image.Image], int]:
    GIF = Image.open(filepath)
    frames: List[Image.Image] = []
    total_duration = 0
    for frame_number in range(GIF.n_frames):
        GIF.seek(frame_number)
        total_duration += GIF.info["duration"]
        frames.append(GIF.copy())
    GIF.close()
    return (frames, total_duration//GIF.n_frames)





def random_string(n):
    result = ""
    for _ in range(n):
        result += random.choice(string.ascii_letters)
    return result

def main():
    root = Tk()
    filepath = StringVar()
    root.title("GIF captioner")
    caption_text = StringVar()

    font_size = StringVar(root, "medium")

    def openFile():
        filepath.set(askopenfilename(filetypes=(("GIF Files", "*.gif"), ("All Files", "*.*"))))

    def captionGIF():

        text = caption_text.get()

        if filepath.get() == "":
            messagebox.showwarning("No file selected")
        
        if text == "":
            messagebox.showwarning("No caption entered")

        frames, frame_duration = GIF_to_sequence(filepath.get())

        for i in range(len(frames)):
            frames[i] = frames[i].convert("RGBA")
            frames[i] = white_bg(frames[i], text, font_size.get())
            frames[i] = add_caption(frames[i], text, font_size.get())

        save_gif(frames, path.dirname(filepath.get())+"/captioned_"+random_string(5)+".gif", frame_duration)

    canvas = Canvas(root, width=500, height=500)
    canvas.pack()

    caption = Entry(root, textvariable=caption_text)
    canvas.create_window(250, 200, window=caption)

    radio_button_1 = Radiobutton(root, text = "Font size: small", variable=font_size, value="small")
    radio_button_2 = Radiobutton(root, text = "Font size: medium", variable=font_size, value="medium")
    radio_button_3 = Radiobutton(root, text = "Font size: large", variable=font_size, value="large")

    canvas.create_window(250, 100, window=radio_button_1)
    canvas.create_window(250, 125, window=radio_button_2)
    canvas.create_window(250, 150, window=radio_button_3)

    open_file_button = Button(root, text="Open File", command=lambda: openFile())
    canvas.create_window(250, 25, window=open_file_button)

    caption_button = Button(root, text="Caption!", command=lambda: captionGIF())
    canvas.create_window(250, 275, window=caption_button)

    opened_file_text = Label(root, textvariable=filepath)
    canvas.create_window(250, 350, window=opened_file_text)

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except:
        exit()