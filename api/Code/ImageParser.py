from random import random

import cv2
import math

from api.Code.CharacterSegmentation import CharacterSegmentation
from api.Code.Predict import Predict
from api.Code.RowSegmentation import RowSegmentation
from api.Code.ColSegmentation import ColSegmentation
from api.Code.WordSegmentation import WordSegmentation


class ImageParser:
    def __init__(self):
        self.predict= Predict()


    def parse(self,image):
        row_segment = RowSegmentation(image)
        rows = row_segment.row_segmentation()
        sheet = []
        #count = 0
        for row in rows:
            # cv2.imwrite('output/rows/' + str(count) + ".png", row)
            # count = count + 1
            col_segment = ColSegmentation()
            columns = col_segment.col_segmentation(row)
            sheet.append(self.row_parser(columns))
        return sheet

    def word_parser(self,chars):
        col_txt=''
        for char in chars:
            char_text = self.predict.predict(char)
            col_txt = col_txt + char_text
            #cv2.imwrite('output/characterSegmentation/' + str(count) + char_text + ".png", char)
            #count = count + 1
        col_txt = col_txt + ' '
        return col_txt

    def sentence_parser(self,words):
        col_txt=''
        for word in words:
            # cv2.imwrite('output/wordSegmentation/' + str(count) + ".png", word[1])
            # cv2.imwrite('output/wordSegmentation/' + str(count) + "_thinning.png", word[0])
            # count = count + 1
            char_segment = CharacterSegmentation(word[0], word[1])
            chars = char_segment.character_segmentation()
            col_txt += self.word_parser(chars)
        return col_txt.lower()

    def row_parser(self,columns):
        sheet_col=[]
        for col in columns:
            # cv2.imwrite('output/cols/' + str(count) + ".png", col[1])
            # cv2.imwrite('output/cols/' + str(count) + "_thinning.png", col[0])
            # count = count + 1
            word_segment = WordSegmentation(col[0], col[1])
            words = word_segment.word_segmentaion()
            sheet_col.append(self.sentence_parser(words))
        return sheet_col