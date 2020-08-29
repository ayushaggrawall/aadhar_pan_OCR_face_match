'''Written by
Ayush Agrawal
'''

import pytesseract
import io
import json
import re
import ftfy
from PIL import Image
import argparse
import cv2
import os
import random

class name:
    def __init__(self):
        pass
    def get_grayscale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    def findword(self,textlist, wordstring):
        lineno = -1
        for wordline in textlist:
            xx = wordline.split( )
            if ([w for w in xx if re.search(wordstring, w)]):
                lineno = textlist.index(wordline)
                textlist = textlist[lineno+1:]
                return textlist
        return textlist

    def text(self,path):
        # cu = "-l eng --oem  1 --psm 4"
        # text = pytesseract.image_to_string(Image.open(path), config = cu)
        # cu = "-l eng --oem  1 --psm 4"
        image=cv2.imread(path)
        image=self.get_grayscale(image)
        text = pytesseract.image_to_string(image)
        # print(path)
        # print(text)


        text_output = open('outputbase.txt', 'w', encoding='utf-8')
        text_output.write(text)
        text_output.close()
        file = open('outputbase.txt', 'r', encoding='utf-8')
        text = file.read()

        # Cleaning all the gibberish text
        text = ftfy.fix_text(text)
        text = ftfy.fix_encoding(text)
        name = None
        fname = None
        dob = None
        pan = None
        nameline = []
        dobline = []
        panline = []
        text0 = []
        text1 = []
        text2 = []

        # Searching for PAN
        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = lin.replace('\n','')
            s = s.rstrip()
            s = s.lstrip()
            text1.append(s)

        text1 = list(filter(None, text1))
        lineno = 0  # to start from the first line of the text file.

        for wordline in text1:
            xx = wordline.split('\n')
            if ([w for w in xx if re.search('(INCOMETAXDEPARWENT @|mcommx|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
                text1 = list(text1)
                lineno = text1.index(wordline)
                break
        try:

            text0 = text1[lineno+1:]
            name = text0[0]
            name = name.rstrip()
            name = name.lstrip()
            name = name.replace("8", "B")
            name = name.replace("0", "O")
            name = name.replace("6", "G")
            name = name.replace("1", "I")
            name = re.sub('[^a-zA-Z] +', ' ', name)
        except:
            pass
        try:
            fname = text0[1]
            fname = fname.rstrip()
            fname = fname.lstrip()
            fname = fname.replace("8", "B")
            fname = fname.replace("0", "O")
            fname = fname.replace("6", "G")
            fname = fname.replace("1", "I")
            fname = re.sub('[^a-zA-Z] +', ' ', fname)
        except:
            pass
        try:
            dob = text0[2]
            dob = dob.rstrip()
            dob = dob.lstrip()
            dob = dob.replace('l', '/')
            dob = dob.replace('L', '/')
            dob = dob.replace('I', '/')
            dob = dob.replace('i', '/')
            dob = dob.replace('|', '/')
            dob = dob.replace('o', '0')
            dob = dob.replace('O', '0')
            dob = dob.replace('f', '1')
            # dob = dob.replace('\"', '/1')
            dob = dob.replace(" ", "")
        except:
            pass
        try:
            text0 = self.findword(text1, '(Pormanam|Number|umber|Account|ccount|count|Permanent|ermanent|manent|wumm)$')
            panline = text0[0]
            pan = panline.rstrip()
            pan = pan.lstrip()
            pan = pan.replace(" ", "")
            pan = pan.replace("\"", "")
            pan = pan.replace(";", "")
            pan = pan.replace("%", "L")
          

        except:
            pass
        data = {}
        try:
            data['Name'] = name
        except:
            pass
        try:
            data['Father Name'] = fname
        except:
            pass
        try:
            if(len(dob)==10 and '/' in dob):
                data['Date of Birth'] = dob
        except:
            pass
        try:
            if(len(pan)==10):
                data['PAN'] = pan
        except:
            pass
        return data
