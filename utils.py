from tkinter import OFF
from typing import List
from PIL import Image, GifImagePlugin, ImageDraw, ImageFont
from sympy import re

OFFSET = 10 # Pixel offset from edges to text
FONTS = {
    "small": ImageFont.truetype("comic.ttf", 12),
    "medium": ImageFont.truetype("comic.ttf", 24),
    "large": ImageFont.truetype("comic.ttf", 48)
}

"""
Saves the provided list of PIL Image objects as a GIF
"""
def save_gif(images: List[Image.Image], filepath):
    try:
        images[0].save(filepath, save_all=True, append_images=images[1:], optimize=True, duration=50, loop=0)
        print("[SUCCESS] GIF saved")
    except:
        print("[FATAL ERROR] GIF export failed")

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
def GIF_to_sequence(filepath: str) -> List[Image.Image]:
    GIF = Image.open(filepath)
    frames: List[Image.Image] = []
    for frame_number in range(GIF.n_frames):
        GIF.seek(frame_number)
        frames.append(GIF.copy())
    GIF.close()
    return frames
