import numpy as np
import cv2 
import argparse
import time
import datetime
from helper import *
from tensorflow.keras.models import model_from_json
import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

### FireBase Authentication
credential_path = os.getcwd() + "/Auth/ccpsl-1797d-firebase-adminsdk-333t0-02b1f5b581.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
### Initializing Firebase App

try: 
    print("Authenticating and Reinitializing Firebase App")
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'ccpsl-1797d.appspot.com'
        })
    db = firestore.client()
except: 
    print("Error Connecting to Firebase")
    print("Check Internet Connection")
    try: 
        print("Authenticating and Reinitializing Firebase App")
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'ccpsl-1797d.appspot.com'
            })
        db = firestore.client()
    except: 
        print("Problem Persists Moving on")

### Command Line Arguments 
parser = argparse.ArgumentParser()
parser.add_argument("IP", help = "Ip address of camera", type = str)
parser.add_argument("SupressDisplay", help = "Whether or not to suppress the display", type = bool)
args = parser.parse_args()

### Load Model
# json_file = open('Models/smally_rack_model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)

# # load weights into new model
# loaded_model.load_weights("Models/smally_rack_model.h5")


###### model from weights ######
loaded_model = RackNet()
loaded_model.load_weights('Models/checkpoints/smally_rack_net_chkpt')
#loaded_model.predict(np.expand_dims(img, axis = 0))

###### Model from pb file ######
# loaded = tf.saved_model.load("Models/rack_net/1/")
# print(list(loaded.signatures.keys()))  #["serving default"]
# infer = loaded.signatures["serving_default"]
# print(infer.structured_outputs)

###### 

print("Loaded model from disk...")

### Predefined Region (Not to be changed for guaranteed performance)
r1 = (150, 368, 63, 41)
### Address to video stream
ip = 'Videos/rack.mp4' ### Test Video
### Vdeo streaming Object
cap = cv2.VideoCapture(ip) 

SupressDisplay = False
isRegionSelected = 1
rack_count = 0
palette_count = 0
p1_change = False
font = cv2.FONT_HERSHEY_SIMPLEX

count_start_time = datetime.datetime.now() ### Needs to change 
count_update_minute_start = datetime.datetime.now()
daily_reset_flag = False 
daily_delta = datetime.timedelta(days = 1)
minute_delta = datetime.timedelta(minutes = 1)
out_dict  = {'Start Date and Time': [],'End Date and Time':[], 
             'Total Rack Count':[],'Total Palette Count':[]} 
while(True): 
    # Capture frames in the video 
    ret, frame = cap.read() 
    frame1 = cv2.cvtColor(np.copy(frame), cv2.COLOR_BGR2RGB)
    if (isRegionSelected == 0):
        # Select ROI
        r1 = cv2.selectROI(frame)
        # Crop image
        imCrop1 = frame1[int(r1[1]):int(r1[1]+r1[3]), int(r1[0]):int(r1[0]+r1[2])]
        #############################################################################
        isRegionSelected = 1

    ### Model Prediction
    p1 = cropAndPredict(frame1, r1, loaded_model)
    frame = cv2.rectangle(frame,
                          (int(r1[0]),int(r1[1])),
                          (int(r1[0] +r1[2]),int(r1[1]+r1[3])),
                          (255, 0, 0), 2
                         )
    ############################################################################
    
    if (p1>0.80):# describe the type of font 
        # to be used. 
  
        # Use putText() method for 
        # inserting text on video 
        cv2.putText(frame,  
                    'No Rack detected at p1 {}'.format(p1),  
                    (100, 100),  
                    font, 0.5,  
                    (0, 255, 255),  
                    2,  
                    cv2.LINE_4)
        check_change = 0
        if(p1_change == True):
            rack_count = rack_count +1
            p1_change = False
         
    elif( p1<0.2):
        # Use putText() method for 
        # inserting text on video 
        cv2.putText(frame,  
                    'Rack detected at p1 \n.{}'. format(p1),  
                    (100, 100),  
                    font, 0.5,  
                    (0, 255, 255),  
                    2,  
                    cv2.LINE_4)
        p1_change = True
        
    # Use putText() method for 
    # inserting text on video 
    cv2.putText(frame,  
                'Racks counted {}'. format(rack_count),  
                (170, 170),  
                font, 0.5,  
                (0, 255, 255),  
                2,  
                cv2.LINE_4)
    ########################################################################
    ### Updates
    #######################################################################
    
    ### History Update 
    #if((datetime.datetime.now()-count_start_time)>daily_delta):
    if((time.localtime(time.time()).tm_mday ==7)and(daily_reset_flag == False)):
        print("Reseting LPU System .....")
        out_dict['Start Date and Time'].append(count_start_time)
        out_dict['End Date and Time'].append(datetime.datetime.now())
        out_dict['Total Rack Count'].append(rack_count)
        out_dict['Total Palette Count'].append(palette_count)### Not implemted
        updateHistory(out_dict)

        ### Reinstantiate Output Dictionary
        out_dict  = {
            'Start Date and Time': [],
            'End Date and Time':[],
            'Total Rack Count':[],
            'Total Palette Count':[]
            }
        
        ### Update Firebase Database with daily summary
        try:
            bucket = storage.bucket()
            blob = bucket.blob("LPU/lpuHistory.pdf")
            blob.upload_from_filename("lpuHistory.pdf")
        except:
            print("Error Connecting to Firebase")
            print("Attemting to reconnect to Firebase Database")
            try:
                ### Reinitialise fibase app
                print("Connecting.... ")
            except:
                print("Problem persists Moving on")      
         
        ### Reset start daily time
        count_start_time = count_start_time + daily_delta
        daily_reset_flag = True
        print("..............Finished.............")

    if(time.localtime(time.time()).tm_mday == 1):
        daily_reset_flag = False

    ### Count update
    if((datetime.datetime.now()-count_update_minute_start)>minute_delta):
        print("Updating count.........")
        print("Rack Count:",rack_count)
        print("Palette Count: Not implemeted")

        try:
            doc_ref = db.collection(u'counts').document(u'lpu_counts')
            doc_ref.set({
                u'count_reset': '{}'.format(datetime.datetime.now().strftime("%H:%M")),
                u'rack_count': '{}'.format(rack_count),
                u'palette_count': '{}'.format(palette_count)
                })
        except:
            print("Error Connecting to Firebase")
            print("Attemting to reconnect to Firebase Database")
            try:
                ### Reinitialise fibase app
                print("Connecting.... ")
            except:
                print("Problem persists Moving on")   

        ### Reset minute start time 
        count_update_minute_start = datetime.datetime.now()

    #######################################################################
    # Display the resulting frame 
    if(SupressDisplay == False):
        cv2.imshow('video', frame) 

    # Set 'q' as the quit  
    # button for the video 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# release the cap object 
cap.release() 
# close all windows 
cv2.destroyAllWindows() 