import cv2
import numpy as np
import numpy as np
import tflite_runtime.interpreter as tflite
import RPi.GPIO as GPIO
from time import sleep
import os

import pyrebase
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 50)
p.start(0)


from PIL import Image

interpreter = tflite.Interpreter(model_path = "model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


cap = cv2.VideoCapture(0)

img_counter = 0
time_counter = 0
checked = False
object1_count = 0
object2_count = 0

###--initialize_app()--###
new_value = 1;
image1 = []
image2 = []
config = {
  "apiKey": "AIzaSyB1uP4DsDSMBozaRrd6FnHPIHh0w8f_09s",
  "authDomain": "doancuoiki-fbe75.firebaseapp.com",
  "databaseURL": "https://doancuoiki-fbe75-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "doancuoiki-fbe75",
  "storageBucket": "doancuoiki-fbe75.appspot.com",
  "messagingSenderId": "1081384755404",
  "appId": "1:1081384755404:web:ca2c030f6fd6d9220f2269",
  "measurementId": "G-5NVV2SNWSE",
  "serviceAccount": "service.json"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
email = "oppahd96@gmail.com"
password = "minhhieu"
user = auth.sign_in_with_email_and_password(email, password)
storageFB = firebase.storage()


# Fetch the service account key JSON file contents
cred = credentials.Certificate('service.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://doancuoiki-fbe75-default-rtdb.asia-southeast1.firebasedatabase.app'
})
for i in range(1,50):
  ref = db.reference(str(i))
  if ref.get() == None:
    new_value = i
    break

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H:%M")
getDay = now.strftime("%d/%m/%Y")
getTime = now.strftime("%H:%M")
##########################

for i in range(1,50):
    my_image1 = "logo1/image1"+str(i)+".jpg"
    try:
        os.remove(my_image1)
        print(my_image1)
    except:
        break

for i in range(1,50):
    my_image1 = "logo2/image2"+str(i)+".jpg"
    try:
        os.remove(my_image1)
        print(my_image1)
    except:
        break

while True:
    time_counter +=1
    print(time_counter)
    p.ChangeDutyCycle(2.5)
    if((object1_count + object2_count)>0 and time_counter>500 ):
        object1_count=0
        object2_count=0
        #####################
        for i in range(1,200):
          my_image1 = "./logo1/image1"+str(i)+".jpg"
          # Upload Image
          try:
            storageFB.child(dt_string+my_image1).put(my_image1)
            url = storageFB.child(dt_string+my_image1).get_url(user['idToken'])
            image1.append(url)
          except:
            break
        for i in range(1,200):
          my_image2 = "./logo2/image2"+str(i)+".jpg"
          # Upload Image
          try:
            storageFB.child(dt_string+my_image2).put(my_image2)
            url = storageFB.child(dt_string+my_image2).get_url(user['idToken'])
            image2.append(url)
          except:
            break

        #calculation rate
        rate1 = len(image1)/(len(image1)+len(image2))*100
        rate2 = len(image2)/(len(image1)+len(image2))*100

        ref = db.reference(str(new_value))
        ref.set({
              "date": getDay,
              "logo1": {
                "1": {
                  "logo":image1[0]
                }
              },
              "logo2": {
                "1": {
                  "logo":image2[0]
                }      
              },
              "ratelogo1": str("{:.2f}".format(rate1)),
              "ratelogo2": str("{:.2f}".format(rate2)),
              "time": getTime
        })

        for i in range(0,len(image1)):
          hopper_ref = ref.child('logo1')
          hopper_ref.update({
              str(i): {
                "logo":image1[i]
              }
          })
        for i in range(0,len(image2)):
          hopper_ref = ref.child('logo2')
          hopper_ref.update({
              str(i): {
                "logo":image2[i]
              }
          })
        #####################
        for i in range(1,50):
            my_image1 = "logo1/image1"+str(i)+".jpg"
            try:
                os.remove(my_image1)
                print(my_image1)
            except:
                break

        for i in range(1,50):
            my_image1 = "logo2/image2"+str(i)+".jpg"
            try:
                os.remove(my_image1)
                print(my_image1)
            except:
                break
        #####################
    _, frame = cap.read()
    
    gray_belt = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_belt, 100, 255, cv2. THRESH_BINARY)
    
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        area = cv2.contourArea(cnt)
        
        if area > 30000:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2. putText(frame, str(area), (x,y), 1, 1, (0, 255, 0))
            img_counter += 1
            print(img_counter)
            if(img_counter > 35) and checked == False:
                img_name = "opject/object.jpg".format()
                cv2.imwrite(img_name, frame)
                
                img = Image.open('opject/object.jpg')
                img = img.resize((150,150))
                img = np.reshape(img, [1,150,150,3])
                img = img.astype(np.float32)
                img = img/255.
                interpreter.set_tensor(input_details[0]['index'], img)
                interpreter.invoke()

                output_data = interpreter.get_tensor(output_details[0]['index'])
                if 1- output_data > output_data:
                    print("logo1")
                    img_info = "info/object1.jpg".format()
                    cv2.imwrite(img_info, frame)
                    img_info2 = "info/threshold1.jpg".format()
                    cv2.imwrite(img_info2, threshold)
                    object1_count += 1
                    img_data = "logo1/image1"+str(object1_count)+".jpg".format()
                    cv2.imwrite(img_data, frame)
                else:
                    print("logo2")
                    img_info = "info/object2.jpg".format()
                    cv2.imwrite(img_info, frame)
                    img_info2 = "info/threshold2.jpg".format()
                    cv2.imwrite(img_info2, threshold)
                    
                    object2_count += 1
                    img_data = "logo2/image2"+str(object2_count)+".jpg".format()
                    cv2.imwrite(img_data, frame)
                    checked = True
                    #print("Checked: ", checked)
                
                print("{} written!".format(img_name))
                img_counter = 0
                time_counter = 0

        if checked == True:
            img_counter += 1
            #print(img_counter)
            if(img_counter > 35):
#                 for n in range(6, 11, 1):
#                     p.ChangeDutyCycle(n)
#                     sleep(0.5)
#                 for n in range(11, 6, -1):
#                     p.ChangeDutyCycle(n)
#                     sleep(0.5)
                sleep(3.75)
                p.ChangeDutyCycle(2.5)
                sleep(0.25)
                p.ChangeDutyCycle(5)
                sleep(0.25)
                p.ChangeDutyCycle(7.5)
                sleep(0.25)
                p.ChangeDutyCycle(10)
                sleep(0.25)
                p.ChangeDutyCycle(7.5)
                sleep(0.25)
                p.ChangeDutyCycle(5)
                sleep(0.25)
                p.ChangeDutyCycle(2.5)
                sleep(0.5)
                img_counter = 0
                checked = False
                #print("Checked: ", checked)
                
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Frame gray", threshold)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
p.stop()
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()