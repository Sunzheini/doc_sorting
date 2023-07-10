import cv2
import numpy as np
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance


file_path = r'C:/Users/User/Desktop/P1/mark-21_268-viking-vert_plan_sklad_new_06_02_2019-v2(2).pdf'


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    page = doc[0]  # get the first page
    rect = fitz.Rect(550, 450, 650, 550)  # x1, y1, x2, y2


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


    # # Convert image to grayscale and apply Gaussian blur and adaptive threshold using OpenCV
    # img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    # img_cv = cv2.GaussianBlur(img_cv, (5, 5), 0)
    # img_cv = cv2.adaptiveThreshold(img_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #
    # # Convert back to PIL Image
    # img = Image.fromarray(img_cv)


    img.show()


    # # Specify Tesseract configuration options
    # config = '--oem 3 --psm 6'


    # Specify Tesseract configuration options
    config = '--oem 3 --psm 6 -l bul'  # Add Bulgarian language

    text = pytesseract.image_to_string(img, config=config)
    return text


print(extract_text_from_pdf(file_path))
