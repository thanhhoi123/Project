import pyrebase
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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