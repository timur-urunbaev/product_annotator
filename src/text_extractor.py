import numpy as np
import easyocr
import cv2

from config import logger


class TextExtractor:

    def __init__(self):
        self.reader = easyocr.Reader(['en'])
    
    def get_suggestions_from_image(self, image_filepath):
        """
        Getting list of suggested words from the image
        
        Args:
            image: PIL Image object
        Returns:
            list: list of words suggestions
        """
        image = cv2.imread(image_filepath) 
        logger.log(
            "INFO",
            f"Extracting text suggestions from the image: {image_filepath}",
            extra={"module": "text_extractor.py"}
        )
        
        results = self.reader.readtext(image)
        suggestions = [result[1] for result in results]

        return suggestions
        