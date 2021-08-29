import os
import cv2
from PIL import Image
import pdf2image as p2i
import pytesseract as pt
import numpy as np


def ocr_from_image(file_path):
    '''
    Optical Character Recognition from image files to text.
    '''
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)
    output = pt.image_to_string(img)
    return output


def ocr_from_pdf(file_path):
    '''
    Optical Character Recognition from PDF files to text.
    '''
    doc = p2i.convert_from_path(file_path)
    path, fileName = os.path.split(file_path)
    fileBaseName, fileExtension = os.path.splitext(fileName)
    whole_txt = ''
    for page_number, page_data in enumerate(doc):
        txt = pt.image_to_string(page_data)
        whole_txt += txt
    return whole_txt

def process(file_path, source='pdf'):
    '''
    Runs OCR process depending on the input file format

    source='img' : image file
    source='pdf' : pdf file
    '''
    if source == 'img':
        return ocr_from_image(file_path)

    else:
        return ocr_from_pdf(file_path)