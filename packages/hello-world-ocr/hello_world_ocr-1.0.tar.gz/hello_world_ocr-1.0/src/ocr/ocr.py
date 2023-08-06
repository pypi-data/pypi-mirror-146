import numpy as np
import re
from pytesseract import image_to_string

def scan(filename):
	return image_to_string('article.png')
