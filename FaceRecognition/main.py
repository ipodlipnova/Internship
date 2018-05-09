from __future__ import print_function
import cognitive_face as CF
import cv2
import requests
import time
from PIL import Image
from io import BytesIO
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
KEY = '' # add your key
BASE_URL = '' # add your base url
URL_DETECT = '' # add your detect url

CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)
endpoint = URL_DETECT

args = {'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender'}
headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': KEY}


# method to detect number of faces on image
def count_number_faces(image):
    face = CF.face.detect(image)
    print(face)
    print("Number of faces on image: " + str(len(face)))
    for i in face:
        print(i['faceId'])


# this method is used to create group of persons, for example 'clients' or 'staff'
def create_group(group_id):
    CF.large_person_group.create(group_id)


# this method is used to add person to a group and assign an image to this person
def add_person_to_group(group_id, name, image):
    CF.large_person_group_person.create(group_id, name)
    face = CF.face.detect(image)
    person_id = CF.large_person_group_person.create(group_id, name)
    CF.large_person_group_person_face.add(image, group_id, person_id['personId'])


# this method is used to find if face from webcam identity with persons from the group
def verify(img):
    f = BytesIO()
    Image.fromarray(img).save(f, 'png')
    data = f.getvalue()
    response = requests.post(data=data,url=endpoint,headers=headers,params=args)
    print(response.json())

    # compare images from group with image from web cam and return result ranked by similarity confidence
    result = CF.face.identify(response.json()[0]['faceId'].split(' '), large_person_group_id='clients')
    print(result)
    if len(result[0]['candidates']) > 0:
        color = [0, 255, 0]
        top, bottom, left, right = [10] * 4
        img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    else:
        color = [0, 0, 255]
        top, bottom, left, right = [10] * 4
        img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return img_with_border


print(CF.large_person_group_person.list('clients'))
# need to train the group before starting identify persons
CF.large_person_group.train('clients')
print(CF.large_person_group.get_status('clients'))

# capture image from web cam
cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    cv2.imshow('img', verify(img))
    if cv2.waitKey(1) == 27:
        break
    time.sleep(.5)
cv2.destroyAllWindows()
cam.release()



