import cv2
import pytesseract
import os
import re
import numpy as np
from storage.s3_upload import upload_s3
import random
import pathlib
import string


def clock90(upload_file,idproof):
    img=cv2.imread(idproof)
    img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(upload_file, img_rotate_90_clockwise)

def anticlock90(upload_file,idproof):
    img=cv2.imread(idproof)
    img_rotate_90_counterclockwise = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(upload_file, img_rotate_90_counterclockwise)

def upside(upload_file,idproof):
    img=cv2.imread(idproof)
    img_rotate_180 = cv2.rotate(img, cv2.ROTATE_180)
    cv2.imwrite(upload_file, img_rotate_180)

def dilate(image):
    kernel = np.ones((2,2),np.uint8)
    return cv2.dilate(image, kernel, iterations = 2)

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

def opening(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def erode(image):
    kernel = np.ones((2,2),np.uint8)
    return cv2.erode(image, kernel, iterations = 2)

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


# path_load='/home/valuepitch/Desktop/Selfie (copy)/198'
def orientation(idproof,file_name,s3_upload=True):

    try:
        img = cv2.imread(idproof, cv2.IMREAD_COLOR)
        img=get_grayscale(img)
        img=dilate(img)        
        newdata=pytesseract.image_to_osd(img)
        arr=newdata.split('\n')
        rotate=int(arr[2][8:])
        pathlib.Path('./image_folder/'+file_name+'_folder/').mkdir(parents=True, exist_ok=True)
        upload_file='./image_folder/'+file_name+'_folder/'+file_name+'.jpg'
        print("$$$$$$$$$$$$$$$")
        print(rotate)
        if rotate==270:
            anticlock90(upload_file,idproof)
        elif rotate==90:
            clock90(upload_file,idproof)
        elif rotate==180:
            upside(upload_file,idproof)
        elif rotate==0:
            return("INPUT IMAGE ORIENTATION CORRECT")
        
        
        if s3_upload:
                s3link, filename = upload_s3(upload_file)
                return s3link
        else:
                return upload_file
        return 0
            
    except Exception as e :
        print('-----------')
        print(e)
        print('-----------')
        return -1
