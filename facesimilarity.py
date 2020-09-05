import face_recognition
import numpy as np
import math
import io
from facerotation import rotation_image_1, rotation_image_2

def img_input(path_1, path_2):
    # global known_encoding
    # global unknown_encoding
    known_image = face_recognition.load_image_file(path_1)
    # print(known_image)
    unknown_image = face_recognition.load_image_file(path_2)
    # print(unknown_image)
    
    try:
        known_encoding = face_recognition.face_encodings(known_image)[0]
        print("---------- ENCODING IMAGE 1----------",known_encoding)
    except IndexError:
        print("No Face found " + "known_image")
        return False, 2, False

    else:
        print(known_encoding)
        pass    
    
    try:
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        print("---------- ENCODING IMAGE 2----------",unknown_encoding)
    except IndexError:
        print("No Face found " + " unknown_image")
        return False, 3, False

    
    else:
        print(unknown_encoding)
        pass    

    return True,known_encoding, unknown_encoding
    # return True


################################ Distance bw faces ###############################

def face_distance(face_encodings, face_to_compare):
    # global distance
    if len(face_encodings) == 0:
        return np.empty((0))

    distance = (np.linalg.norm(face_encodings - face_to_compare, axis=0))
    print("distance",distance)
    return distance
    # return True

############################## Similarity score bw faces###########################

def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = int(((1.0 - face_distance) / (range * 2.0))*100)
        print("Similarity is :")
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        linear_val= int((linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2)))*100)
        print("Similarity is :")
        return linear_val


def main_process(path_1,path_2):
    #known_encoding, unknown_encoding=img_input(path_1="/Users/apple/Desktop/virat/viratcasual.jpeg", path_2="/Users/apple/Desktop/virat/viratoldsuit.jpeg")

    rotation_image_1(abs_img_src=path_1)
    rotation_image_2(abs_img_src_1=path_2)



    try:
        face_status, known_encoding, unknown_encoding=img_input(path_1, path_2)
        if not face_status:
            if known_encoding==2:
                print('[x] IN 1st condition-------------------')
                print(known_encoding, unknown_encoding)

                '''No Face In 1st Image'''
                return {'status':2, 'score':None}

            elif known_encoding==3:
                print('[x] IN 2nd condition-------------------')
                print(known_encoding, unknown_encoding)

                '''No face in 2nd image'''
                return {'status':3, 'score':None}

        else:
            '''Face Found'''
            print(known_encoding, unknown_encoding)
            distance=face_distance(face_encodings=known_encoding,face_to_compare=unknown_encoding)
            
            similarity_score=face_distance_to_conf(face_distance=distance) 
            
            return {'status':1,'score':similarity_score}
    
    except Exception as e: 
        print('ERROR in main_process',  e)
        return {'status':0, 'score':None}

        

