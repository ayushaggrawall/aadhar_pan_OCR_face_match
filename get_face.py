'''Written by
Ayush Agrawal
'''

from mtcnn.mtcnn import MTCNN
import cv2
import os
import numpy as np
import random
import pathlib
import string
from storage.s3_upload import upload_s3

class FaceManager:
    def __init__(self):
        self.detector = MTCNN()
    def id_generator(self,size=10, chars=string.ascii_uppercase + string.digits):
        """
        Creates the unique String ID
        """
        return "".join(random.choice(chars) for _ in range(size))
    def extract_face(self, idproof,file_name,s3_upload=True):
        try:
            image = cv2.cvtColor(cv2.imread(idproof), cv2.COLOR_BGR2RGB)
            result = self.detector.detect_faces(image)
            x=[]
            for i in range(0,len(result)):
                if(result[i]['confidence']>0.85):
                    x.append(result[i]['box'])
            img=cv2.imread(idproof)
            data=[]
            for i in range(len(x)):
                x_cord=x[i][0]
                width=x[i][2]
                y_cord=x[i][1]
                height=x[i][3]
                y_low=int(y_cord-(height/2))
                if(y_low<=0):
                    y_low=0
                x_low=int(x_cord-(width/2))
                if(x_low<=0):
                    x_low=0
                crop_img = img[y_low:int(y_cord+height+(height/2)),x_low:int(x_cord+width+(width/2))]
                
                pathlib.Path('./image_folder/'+file_name+'_folder/').mkdir(parents=True, exist_ok=True)
                upload_file='./image_folder/'+file_name+'_folder/'+file_name+'_'+str(i)+'.jpg'
                cv2.imwrite(upload_file, crop_img)
                if s3_upload:
                    s3link, filename = upload_s3(upload_file)
                    data.append(s3link)
                    print('################')
                    print(filename)
                    print('################')

                else:
                    print("FILE STORED IN LOCAL SERVER")
            return data
        except Exception as e:
            print("ERROR")
            print(e)
            return False


