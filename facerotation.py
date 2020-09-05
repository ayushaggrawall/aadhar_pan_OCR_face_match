from PIL import Image
import sys
import face_recognition

# abs_img_src = '/Users/apple/Desktop/Screenshot 2019-10-01 at 12.59.28 PM.png'

def rotation_image_1(abs_img_src):
    img = face_recognition.load_image_file(abs_img_src)
    imgg=face_recognition.face_encodings(img)
    # print(imgg)
    if imgg==[]:
    #     print(abs_img_src)
        pill_img = Image.open(abs_img_src)
        rotated_img = pill_img.rotate(90)
        rgb_im = rotated_img.convert('RGB')
        r1=rgb_im.save(abs_img_src)
    #     print(r1)
    #     rotated_img.show()
        img=face_recognition.load_image_file(abs_img_src)
        imgg=face_recognition.face_encodings(img)
    #     print(imgg)
        if imgg==[]:
            pill_img = Image.open(abs_img_src)
            rotated_img = pill_img.rotate(90)
            rgb_im = rotated_img.convert('RGB')
            r1=rgb_im.save(abs_img_src)
    #         print(r1)
    #         rotated_img.show()
            img=face_recognition.load_image_file(abs_img_src)
            imgg=face_recognition.face_encodings(img)
    #         print(imgg)
            if imgg==[]:
                pill_img = Image.open(abs_img_src)
                rotated_img = pill_img.rotate(90)
                rgb_im = rotated_img.convert('RGB')
                r1=rgb_im.save(abs_img_src)
    #             print(r1)
    #             rotated_img.show()
                img=face_recognition.load_image_file(abs_img_src)
                imgg=face_recognition.face_encodings(img)
                return imgg
            else:
                pass
        else:
            pass
    else:
        pass
print("process complete for image 1")    


def rotation_image_2(abs_img_src_1):
    img1 = face_recognition.load_image_file(abs_img_src_1)
    imgg1=face_recognition.face_encodings(img1)
    # print(imgg)
    if imgg1==[]:
    #     print(abs_img_src)
        pill_img = Image.open(abs_img_src_1)
        rotated_img = pill_img.rotate(90)
        rgb_im = rotated_img.convert('RGB')
        r1=rgb_im.save(abs_img_src_1)
    #     print(r1)
    #     rotated_img.show()
        img1=face_recognition.load_image_file(abs_img_src_1)
        imgg1=face_recognition.face_encodings(img1)
    #     print(imgg)
        if imgg1==[]:
            pill_img = Image.open(abs_img_src_1)
            rotated_img = pill_img.rotate(90)
            rgb_im = rotated_img.convert('RGB')
            r1=rgb_im.save(abs_img_src_1)
    #         print(r1)
    #         rotated_img.show()
            img1=face_recognition.load_image_file(abs_img_src_1)
            imgg1=face_recognition.face_encodings(img1)
    #         print(imgg)
            if imgg1==[]:
                pill_img = Image.open(abs_img_src_1)
                rotated_img = pill_img.rotate(90)
                rgb_im = rotated_img.convert('RGB')
                r1=rgb_im.save(abs_img_src_1)
    #             print(r1)
    #             rotated_img.show()
                img1=face_recognition.load_image_file(abs_img_src_1)
                imgg1=face_recognition.face_encodings(img1)
                return imgg1
            else:
                pass
        else:
            pass
    else:
        pass
print("process complete for image 2")    
# rotation_image('/Users/apple/Desktop/Screenshot 2019-10-01 at 12.59.28 PM.png')