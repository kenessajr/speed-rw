# -*- coding: utf-8 -*-
import argparse
import cv2
import numpy as np
import pytesseract
from PIL import Image


def text_localization(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(image, (3, 3), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 50))
    img_bh = cv2.morphologyEx(img_blur, cv2.MORPH_BLACKHAT, kernel)
    # cv2.imshow("Blackhat", img_bh)
    # cv2.waitKey(0)
    # binarization
    _, img_binary = cv2.threshold(img_bh, 0, 255, cv2.THRESH_OTSU)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 10))
    img_close = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel_close)
    # cv2.imshow("closing", img_close)
    # cv2.waitKey(0)

    # find Text areas
    contours, hierarchy = cv2.findContours(
        img_close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas = []
    for contour in contours:
        box = cv2.minAreaRect(contour)
        angle = box[2]
# filtering on the size of the boxes
        if((box[1][0] < 300) or (box[1][1] < 100)):
            continue
        if angle < -45:
            angle = box[1][1] / box[1][0]
        else:
            angle = box[1][0] / box[1][1]

        if angle < 2:
            continue

        areas.append(box)
    # draw detected areas
    image = image.copy()
    for i in range(0, len(areas)):
        color = (0, 255, 0)
        rect = cv2.boxPoints(areas[i])
        rect = np.int0(rect)
        cv2.drawContours(image, [rect], -1, color, 2)

    cv2.imshow("identified text areas", image)
    cv2.waitKey(0)
    return (areas)  # list of areas


def crop(areas):
    cropped_img = []  # list of cropped image, representing text Areas in the img
    for text_area in areas:
        if text_area[2] < -45.0:
            text_area_list = list(text_area)
            angle = text_area_list[2]
            angle += 90.0
            # swap w,h = h,w
            wh = list(text_area[1])
            wh[0], wh[1] = wh[1], wh[0]
            whtup = tuple(wh)
            del text_area_list[1]
            text_area_list.insert(1, whtup)
            text_area = tuple(text_area_list)

        text_cropped = cv2.getRectSubPix(
            img, (int(text_area[1][0] + 7), int(text_area[1][1] + 20)), text_area[0])
        text_cropped = cv2.resize(text_cropped, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        cropped_img.append(text_cropped)

    return(cropped_img)


def text_recognition(cropped_img):
    """ Uses pyTesseract for OCR """
    reco_text = []  # list of recognized text/ tesseract's output
    for img in cropped_img:
        img_pil = Image.fromarray(img)  # pytesseract only takes PIL images
        text = pytesseract.image_to_string(
            img_pil, config='--psm 7')
        reco_text.append(text)
    return(reco_text)


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    arg = vars(ap.parse_args())
    img = cv2.imread(arg["image"])
    cv2.imshow("Input Image", img)
    cv2.waitKey(0)
    # --------------------------------
    text_areas = text_localization(img)
    cropped_img = crop(text_areas)
    for img in cropped_img:
        cv2.imshow("crop", img)
        cv2.waitKey(0)
    text = text_recognition(cropped_img)
    for t in text:
        print(t)


