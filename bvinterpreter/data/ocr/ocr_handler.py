import os
from typing import Dict, List

import cv2
import pandas as pd
import pytesseract
import torch
from pytesseract import Output

from bvinterpreter.data.ocr.image_loader import BaseImageLoader
from bvinterpreter.data.ocr.parser import AbstractParser
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

os.environ['USE_TORCH'] = '1'

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


class MindeeOCR:
    def __init__(self, parser: AbstractParser) -> None:
        self.parser: AbstractParser = parser
        self.ocr_model = ocr_predictor(
            det_arch="db_resnet50_rotation", reco_arch="crnn_vgg16_bn", pretrained=True, assume_straight_pages=True,
        ).cuda()

    def parse(self, filepath: str) -> pd.DataFrame:
        """Parses with ocr the image of a single page

        Args:
            filepath (str): the file path of the image

        Returns:
            pd.DataFrame: The dataframe of the data

        Examples:
            >>> import os
            >>> path: str = os.path.join("tests", "resources", "test.pdf")
            >>> from bvinterpreter.data.ocr.parser import BaseParser
            >>> parser = BaseParser()
            >>> ocr = MindeeOCR(parser)
            >>> res = ocr.parse(path)
        """
        if filepath[-4:] == ".pdf":
            doc = DocumentFile.from_pdf(filepath)
        elif filepath[-4:] == ".jpg":
            doc = DocumentFile.from_images(filepath)
        else:
            raise ValueError(f"File not supported for: {filepath}")
        for i, img in enumerate(doc):
            doc[i] = img.transpose((1, 0, 2))[::-1, :, :]
        doc = [doc[0]]
        ocr_data = self.ocr_model(doc)
        # TODO: finish this part where the text is parsed properly => we have better detections but we need to align each line now
        lines: List = []
        headers: List[str] = ["Elect.", "Noms et prénoms", "Date", "Lieu", "Adresse"]
        for page in ocr_data.pages:
            for b in page.blocks:
                lines += b.lines
        lines_parsed: Dict
        parsed_data = self.parser.parse(text)
        return parsed_data
