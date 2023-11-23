# -*- coding: utf-8 -*-
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance


def extract_text_from_pdf(file_path, coordinates):
    doc = fitz.open(file_path)
    page = doc[0]  # get the first page

    rect = fitz.Rect(coordinates['x1'], coordinates['y1'], coordinates['x2'], coordinates['y2'])  # both tables inside

    # Get a pixmap of the specific area of the page at a higher resolution.
    mat = fitz.Matrix(4, 4)  # Increase the resolution by a factor of 4, more is better but slower
    pix = page.get_pixmap(matrix=mat, clip=rect)

    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)

    # Resize the image for display
    img = img.resize((img.width * 2, img.height * 2), Image.Resampling.BICUBIC)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)

    # img.show()    # if you want to preview the image during development

    # # Specify Tesseract configuration options
    config = '--oem 3 --psm 6'          # better this if no bulgarian language!

    # Specify Tesseract configuration options
    # config = '--oem 3 --psm 6 -l bul'  # Add Bulgarian language if has any!

    text = pytesseract.image_to_string(img, config=config)

    # remove \n and \x0c
    text = text.replace('\n', ' ')
    text = text.replace('\x0c', ' ')

    return text
