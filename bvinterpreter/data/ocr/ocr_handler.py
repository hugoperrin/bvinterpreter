import cv2
import pandas as pd
import pytesseract
from pytesseract import Output

from bvinterpreter.data.ocr.image_loader import BaseImageLoader
from bvinterpreter.data.ocr.parser import AbstractParser


class BaseOCR:
    def __init__(self, parser: AbstractParser) -> None:
        self.parser: AbstractParser = parser

    def parse(self, filepath: str) -> pd.DataFrame:
        """Parses with ocr the image of a single page

        Args:
            filepath (str): the file path of the image

        Returns:
            pd.DataFrame: The dataframe of the data

        Examples:
            >>> import os
            >>> path: str = os.path.join("tests", "resources", "test_image_low.png")
            >>> from bvinterpreter.data.ocr.parser import BaseParser
            >>> parser = BaseParser()
            >>> ocr = BaseOCR(parser)
            >>> res = ocr.parse(path)
        """
        image: cv2.Mat = BaseImageLoader.read(filepath)
        text = pytesseract.image_to_data(image, output_type=Output.DICT, lang="eng+fra")
        parsed_data = self.parser.parse(text)
        return parsed_data
