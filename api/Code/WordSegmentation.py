import cv2
import numpy as np

from api.Code.ImageSegmentation import ImageSegmentation


class WordSegmentation(ImageSegmentation):
    def __init__(self, thinned_image, original_image):
        super(WordSegmentation,self).__init__(thinned_image,original_image)

    def get_first_empty_line(self, loop_range):
        emptyRowIndex = -1
        for row in loop_range:
            whiteBixels = 0
            for col in range(self.width):
                if self.thinned_image[row, col] == 255:
                    whiteBixels += 1

            if whiteBixels == 0:
                emptyRowIndex = row
                break
        return emptyRowIndex

    def remove_empty_lines(self, begin, end):
        self.thinned_image[begin:end, :] = 0
        self.original_image[begin:end, :] = 0

    def remove_horizontal_lines(self):

        # remove below horizontal lines
        emptyRowsBelow = self.get_first_empty_line(range(round(self.height / 2), self.height))
        if (emptyRowsBelow != -1):
            self.remove_empty_lines(emptyRowsBelow, self.height)
        else:
            self.remove_empty_lines(self.height - 2, self.height)

        # remove above horizontal lines
        emptyRowsAbove = self.get_first_empty_line(reversed(range(0, round(self.height / 2))))
        if (emptyRowsAbove != -1):
            self.remove_empty_lines(0, emptyRowsAbove)
        else:
            self.remove_empty_lines(0, 2)

    #TODO Refactor_function
    # def remove_vertical_lines(self, thiningImage):
    #
    #     # cv2.imshow("before",image)
    #     lineColsRight = []
    #     lineColsleft = []
    #     NoOfPixelsCol = []
    #
    #     # remove left Lines
    #     for col in range(len(thiningImage[0])):
    #         whiteBixels = 0
    #         for row in range(len(thiningImage)):
    #             if thiningImage[row, col] == 255:
    #                 whiteBixels += 1
    #
    #         if whiteBixels == 0:
    #             break
    #         else:
    #             lineColsleft.append(col)
    #             NoOfPixelsCol.append(whiteBixels)
    #     for col, NoOFPixel in zip(lineColsleft, NoOfPixelsCol):
    #         if NoOFPixel > 3:
    #             thiningImage[:, col] = 0
    #
    #     # remove right Lines
    #     for col in reversed(range(len(thiningImage[0]))):
    #         whiteBixels = 0
    #         for row in range(len(thiningImage)):
    #             if thiningImage[row, col] == 255:
    #                 whiteBixels += 1
    #
    #         if whiteBixels == 0:
    #             break
    #         else:
    #             lineColsRight.append(col)
    #             NoOfPixelsCol.append(whiteBixels)
    #     for col, NoOFPixel in zip(lineColsRight, NoOfPixelsCol):
    #         if NoOFPixel > 3:
    #             thiningImage[:, col] = 0
    #
    #     return thiningImage

    def removeVerticalLines(self,image):
        # remove left Lines
        image[:, 0:2] = 0
        # remove right Lines
        image[:, len(image[0]) - 2:len(image[0])] = 0

        return image


    def get_empty_sequential_cols_count(self, col_white_pixels, phrase_beginning, phrase_ending):
        empty_sequential_cols_count = []
        counter = 0
        for colIndex in range(phrase_beginning, phrase_ending):
            if col_white_pixels[colIndex] == 0:
                counter = counter + 1
            else:
                if counter > 0:
                    empty_sequential_cols_count.append(counter)
                counter = 0
        return empty_sequential_cols_count

    def get_segmentation_threshold(self):

        col_white_pixels = np.empty(self.width, dtype=np.int8)

        # step1 White Pixel count
        for colIndex in range(self.width):
            white_pixels = 0
            for rowIndex in range(self.height):
                if self.thinned_image[rowIndex, colIndex] == 255:
                    white_pixels += 1
            # arr[colIndex] = white_pixels if white_pixels < 1 else 2
            col_white_pixels[colIndex] = white_pixels

        phrase_beginning, phrase_ending = self.get_boundaries(col_white_pixels)

        countArr = self.get_empty_sequential_cols_count(col_white_pixels, phrase_beginning,
                                                                           phrase_ending)

        countArr.sort()

        threshold = 0
        x = 0
        for i in reversed(range(len(countArr))):
            if countArr[i] - countArr[i - 1] > 15 and i > 1:
                threshold = countArr[i]
                x = 1

        if x == 1:
            return threshold
        else:
            return 1000

    def get_dialation_image(self):
        segmentation_threshold=self.get_segmentation_threshold()
        kernel = np.ones((20,segmentation_threshold ), np.uint8)
        return cv2.dilate(self.thinned_image, kernel, iterations=1)

    def word_segmentaion(self):

        self.thinned_image = self.removeVerticalLines(self.thinned_image)
        self.remove_horizontal_lines()

        # dilation
        img_dilation = self.get_dialation_image()

        # find contours
        im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # sort contours
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

        Words = []
        for i, ctr in enumerate(sorted_ctrs):

            # Get bounding box
            x, y, w, h = cv2.boundingRect(ctr)

            # Getting ROI "Region of intersts"
            roi_original = self.original_image[y:y + h, x:x + w]
            roi2_thining = self.thinned_image[y:y + h, x:x + w]

            # show ROI

            height,width = roi_original.shape
            if (height > 8 and width > 8):
                # cv2.imwrite("output\\wordSegmentation\\" + str(counter()) + ".png", roi_original)
                Words.append((roi2_thining,roi_original))
                #characterSegmentation(roi2_thining, roi_original)
        return Words