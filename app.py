'''Written by
Ayush Agrawal
'''


from flask import request, url_for
from flask import Flask, escape, request, jsonify, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
import tensorflow as tf
from get_face import FaceManager
import base64
import json
import requests
import pathlib
import os
import shutil
from get_data import DataManager
import orient
from facesimilarity import main_process
import cv2
from PIL import Image
from panocr import pan_ocr

# import get_data


main_dir='./'
app = Flask(__name__)
CORS(app)
global sess
global graph
sess = tf.keras.backend.get_session() # Creating tf session(Always running)
graph = tf.compat.v1.get_default_graph()
 
with graph.as_default():
    set_session(sess)
get_face = FaceManager()
get_data = DataManager()
get_data2= pan_ocr()





@app.route("/getface", methods=["POST", "GET"])
def get_gallery():
    rawdata = request.form.to_dict()
    idproof = rawdata.get("idproof")
    # selfie = rawdata.get("selfie")
    # try:
    pathlib.Path(main_dir+'image_folder').mkdir(parents=True, exist_ok=True)
    with graph.as_default():
        set_session(sess)
        file_name = get_face.id_generator()

        filename = "./image_folder/" + file_name
        r = requests.get(str(idproof), allow_redirects=True)
        open(filename, 'wb').write(r.content)
        data=get_face.extract_face(idproof=filename,file_name=file_name)
        path_load="./image_folder/"+file_name+"_folder"
        os.remove(filename)
        try:
            shutil.rmtree(path_load)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        return jsonify(data)
        
@app.route("/getdata", methods=["POST", "GET"])
def get_data_OCR():
    rawdata = request.form.to_dict()
    idproof = rawdata.get("idproof")
   
    pathlib.Path(main_dir+'image_folder').mkdir(parents=True, exist_ok=True)
    with graph.as_default():
        set_session(sess)
        file_name = get_face.id_generator()
        filename = "./image_folder/" + file_name
        r = requests.get(str(idproof), allow_redirects=True)
        open(filename, 'wb').write(r.content)
        
        data=get_data.ocr_text(filename)
        try:
            os.remove(filename)
        except:
            pass
        return jsonify(data)

    # except Exception as e:
    #     responsedata = {"status": -1}
    #     print(e)
    #     return jsonify(responsedata)
@app.route("/pandata", methods=["POST", "GET"])
def get_data_OCR2():
    rawdata = request.form.to_dict()
    idproof = rawdata.get("idproof")
   
    pathlib.Path(main_dir+'image_folder').mkdir(parents=True, exist_ok=True)
    with graph.as_default():
        set_session(sess)
        file_name = get_face.id_generator()
        filename = "./image_folder/" + file_name
        r = requests.get(str(idproof), allow_redirects=True)
        open(filename, 'wb').write(r.content)
        
        data=get_data2.ocr_text(filename)
        try:
            os.remove(filename)
        except:
            pass
        return jsonify(data)
@app.route("/orient", methods=["POST", "GET"])
def get_orientation():
    rawdata = request.form.to_dict()
    idproof = rawdata.get("idproof")
    # selfie = rawdata.get("selfie")
    # try:
    pathlib.Path(main_dir+'image_folder').mkdir(parents=True, exist_ok=True)
    with graph.as_default():
        set_session(sess)
        file_name = orient.id_generator()
        filename = "./image_folder/" + file_name
        r = requests.get(str(idproof), allow_redirects=True)
        open(filename, 'wb').write(r.content)
        data=orient.orientation(idproof=filename,file_name=file_name)
        path_load="./image_folder/"+file_name+"_folder"
        os.remove(filename)
        try:
            shutil.rmtree(path_load)
        except OSError as e:
            return jsonify(data)
        return jsonify(data)


@app.route('/similarity', methods=['GET', 'POST'])
# @cross_origin()
def index():

    rawdata = request.form.to_dict()
    idproof = rawdata["idproof"]
    selfie = rawdata["selfie"]

    pathlib.Path(main_dir+'image_folder').mkdir(parents=True, exist_ok=True)
    with graph.as_default():
        set_session(sess)
        file_name = orient.id_generator()
        filename1 = "./image_folder/" + file_name+'.jpg'
        file_name = orient.id_generator()
        filename2 = "./image_folder/" + file_name+'.jpg'
        r = requests.get(str(idproof), allow_redirects=True)
        open(filename1, 'wb').write(r.content)
        r = requests.get(str(selfie), allow_redirects=True)
        open(filename2, 'wb').write(r.content)

        img_check1=cv2.imread(filename1)
        img_check2=cv2.imread(filename2)
        if img_check1 is None:
            with open(filename1) as f:
                for ix,i in enumerate(f):
                    z=i.index(',')
                    b64=i[z+1:]

            with open(filename1,'wb') as f:
                    f.write(base64.b64decode(b64.encode())) 
        if img_check2 is None:
            with open(filename2) as f:
                for ix,i in enumerate(f):
                    z=i.index(',')
                    b64=i[z+1:]
            with open(filename2,'wb') as f:
                    f.write(base64.b64decode(b64.encode()))
        del(img_check1)         
        del(img_check2)    

        img1=Image.open(filename1)
        rgb_im = img1.convert('RGB')
        rgb_im.save(filename1)
        img2=Image.open(filename2)
        rgb_im = img2.convert('RGB')
        rgb_im.save(filename2)
        del(img1,img2,rgb_im)

        data=main_process(filename1,filename2)
        os.remove(filename1)
        os.remove(filename2)
        return jsonify(data)


if __name__ == "__main__":
    app.run("0.0.0.0",port= 5001,debug=True)
