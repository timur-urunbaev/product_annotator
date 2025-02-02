import os
import sys

import numpy as np

import easyocr
from PIL import Image


class TitleExtractor:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    @staticmethod
    def convert_image_to_array(image):
        """
        Convert PIL Image to numpy array
        Args:
            image: PIL Image object
        Returns:
            np.array: numpy array of the image
        """
        return np.array(image)

    def get_suggestions_from_image(self, image):
        """
        Getting list of suggested words from the image
        Args:
            image: PIL Image object
        Returns:
            list: list of words suggestions
        """
        results = self.reader.readtext(image)
        suggestions = [result[1] for result in results]
        
        return suggestions
