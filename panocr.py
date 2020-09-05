import cv2
import numpy as np
import pytesseract
import orient
import os
import string
import random
import text_ocr
from text_ocr import name
name_new = name()
class pan_ocr:
    def __init__(self):
        pass
    def id_generator(self,size=10, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))
    def get_grayscale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    def dilate(self,image):
        kernel = np.ones((2,2),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)
    def ocr_core(self,filename):
        cu = "-l eng --oem  1 --psm 11"
        image=cv2.imread(filename)
        # image=self.get_grayscale(image)
        image= cv2.medianBlur(image, 3)
        text = pytesseract.image_to_string(image,config=cu)
        return text

    def pancard(self,ocrtext,path):
        result={}
        new_result=name_new.text(path=path)
        for i in ocrtext:
            try:
                if(len(i)==10 and '/' in i):
                    result.update({'DOB:':i})
            except:
                pass
            try:
                if(len(i)==10 and '/' not in i and i.isupper()):
                    result.update({'PAN NUMBER:':i})
            except:
                pass
        check= not bool (result)
        if check==False:
            result.update(new_result)
            return result
        else:
            return new_result
        # if check and repeat:
        #     res=self.reorient(path,repeat=True)
        #     return res
        
    def ocr_text(self,path):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if(img.shape[0]<350):
            try:
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                img.shape
                scale_percent = 280 # percent of original size
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                # resize image
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imwrite(path+'.jpg',resized)
                path=path+'.jpg'
            except:
                print('Error in resizing')


        try:
            text=self.ocr_core(path)
            res=text.split('\n')
            x=[]
        
            for i in res:
                temp=i.replace(' ','')
                temp=temp.replace('-','')
                if temp is not '':
                    x.append(temp)
            pan=-1
            pan2=-1
            for i in x:
                    pan=i.find("INCOME")
                    pan2=i.find("TAX")
                    if(pan>=0 or pan2>=0):
                        break

            if(pan>=0 or pan2>=0 ):
                cu = "-l eng --oem  1 --psm 11"
                image=cv2.imread(path)
                image=self.get_grayscale(image)
                # image=self.dilate(image)
                img= cv2.medianBlur(img, 3)
                text2 = pytesseract.image_to_string(image,config=cu)
                res2=text2.split('\n')
                x2=[]
                for i in res2:
                    temp=i.replace(' ','')
                    temp=temp.replace('-','')
                    if temp is not '':
                        x2.append(temp)
            
                res=self.pancard(x,path)
                res2=self.pancard(x,path)
                # try:
                #     os.remove(path)
                # except:
                #     pass 
                print('-------------------------------------')
                print(x)
                print(x2)
                print('-------------------------------------')

                if(len(res.keys())>len(res2.keys())):
                    return res
                else:
                    return res2    
                return res
        except Exception as e:
            print("ERROR")
            print(e)