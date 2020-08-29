'''Written by
Ayush Agrawal
'''

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
class DataManager:
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
        cu = "-l eng --oem  1 --psm 4"
        image=cv2.imread(filename)
        image=self.get_grayscale(image)
        text = pytesseract.image_to_string(image,config=cu)
        return text
    def anticlock90(self,upload_file,idproof):
        img=cv2.imread(idproof)
        img_rotate_90_counterclockwise = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(upload_file+'.jpg', img_rotate_90_counterclockwise)

    def pancard(self,ocrtext,path,repeat=True):
        result={}
        print('*********')
        print(ocrtext)
        print("REACHING PAN")
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
        if check and repeat:
            res=self.reorient(path,repeat=True)
            return res
        


        return result

    def aadhar_result(self,ocrtext,path,repeat=True,landscape=True):
        
        result={}
        for i in ocrtext:
            try:
                aadhar=int(i)
            except:
                continue
            if len(i)==12:
                result.update({'AADHAAR NUMBER:':aadhar})
                return result
                
        if repeat:
            if landscape:
                print("IN LANDSCAPE")
                self.anticlock90(path,path)
                res=self.ocr_text(path+'.jpg',repeat=True,landscape=False)
                return res
            else:
                res=self.reorient(path,repeat=True)
                return res
        
        return result

    def reorient(self,path,repeat=False):
        try:
            if repeat:
                print("IN REORIENT")
                filename=self.id_generator()
                newimage=orient.orientation(path,filename,s3_upload=False)
                ans=self.ocr_text(newimage,repeat=False,landscape=False)
                return(ans)
        except:
            return {'status':0}


    def ocr_text(self,path,repeat=True,landscape=True):

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
            print(x)
            for i in x:
                    pan=i.find("INCOME")
                    pan2=i.find("TAX")
                    if(pan>=0 or pan2>=0):
                        break
            

            if(pan>=0 or pan2>=0 ):
                cu = "-l eng --oem  1 --psm 4"
                image=cv2.imread(path)
                image=self.get_grayscale(image)
                # image=self.dilate(image)
                text = pytesseract.image_to_string(image,config=cu)
                res=text.split('\n')
                x=[]
                for i in res:
                    temp=i.replace(' ','')
                    temp=temp.replace('-','')
                    if temp is not '':
                        x.append(temp)
                res=self.pancard(x,path,repeat)
                try:
                    os.remove(path)
                except:
                    pass      
                return res

            else:

                res=self.aadhar_result(x,path,repeat,landscape)
                return res

            return 0
            if repeat:

                if landscape:
                    self.anticlock90(path,path)
                    self.ocr_text(path,repeat=True,landscape=False)

                if(x==[]):
                    res=self.reorient(path)
                    return res
            else:
                return{'notfound':0}
        except Exception as e:
            print(e)

                
