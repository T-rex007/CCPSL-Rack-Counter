#!/usr/bin/env python3

import numpy as np
import cv2 
import argparse
import time
import datetime
import firebase_admin
import os
from helper import *
from tensorflow.keras.models import model_from_json
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
### FireBase Authentication
project_id = 'ccpsl-tt'
bucket_path = 'ccpsl-tt.appspot.com'
rel_cred_path = "/Auth2/ccpsl-tt-a3f9d8857c5a.json"
credential_path = os.getcwd() + rel_cred_path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

### Initializing Firebase App
try: 
    print("Authenticating and Initializing Firebase App")
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        #'storageBucket': 'ccpsl-1797d.appspot.com'
        'storageBucket': bucket_path,
        'projectId': project_id
        })
    db = firestore.client()
except: 
    print("Error Connecting to Firebase")
    print("Check Internet Connection")
    try: 
        print("Authenticating and Reinitializing Firebase App")
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'storageBucket': bucket_path,
            'projectId': project_id
            })
        db = firestore.client()
    except: 
        print("Problem Persists Moving on")

### Command Line Arguments 
# RAC
### Load Model
# json_file = open('Models/smally_rack_model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)

# # load weights into new model
# loaded_model.load_weights("Models/smally_rack_model.h5")


###### model from weights ######
loaded_model = RackNet()
loaded_model.load_weights(os.getcwd() + '/Models/checkpoints/smally_rack_net_chkpt')
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
ip = os.getcwd()+'/'+'Videos/rack.mp4' ### Test Video
### Vdeo streaming Object
print("Loading Capture")
cap = cv2.VideoCapture(ip) 
print("Camera Address: " + ip)
print("Finished")

SupressDisplay = False
isRegionSelected = 1
rack_count = 0
palette_count = 0
p1_change = False
font = cv2.FONT_HERSHEY_SIMPLEX

count_start_time = datetime.datetime.now() ### Needs to change 
hour_index_check = time.localtime(time.time()).tm_hour
count_update_minute_start = datetime.datetime.now()
daily_reset_flag = False 
daily_delta = datetime.timedelta(days = 1)
minute_delta = datetime.timedelta(minutes = 1)
out_dict  = {'Start Date and Time': [],'End Date and Time':[], 
             'Total Rack Count':[],'Total Palette Count':[]} 

hourlyLogInit()
print("Reload saved count?")
print("Checking...")

with open(os.getcwd()+'/'+"Count_backup/saved_rack_count.txt", "r") as f:
    r, dr = f.read().split("#")
# with open("Count_backup/saved_palette_count.txt", "r") as f:
#     p, dp = f.read().split("#")

dshutdown = datetime.datetime.strptime(dr, "%Y-%m-%d-%H-%M-%S")
dnow = datetime.datetime.now()

dnow_day = dnow.strftime("%Y-%m-%d")
dnow_time = dnow.strftime("%H-%M-%S")

dshutdown_day = dshutdown.strftime("%Y-%m-%d")
dshutdown_time = dshutdown.strftime("%H-%M-%S")

hms_shutdown =[ int(i) for i in dshutdown_time.split("-")]
hms_now = [int(i) for i in dnow_time.split("-")] 
print("Shutdown Time [hour, minutes, seconds]: ", hms_shutdown)
print("Time [hour, minutes, seconds]: ", hms_now)

for i in range(1):
    if(datetime.timedelta(days = 1)>(dnow-dshutdown)):
        if ((hms_shutdown[0]<7) and (hms_now[0]>=7)):
            ## If the hour at which the system shutdown is before 7am
            ## and the system restarts at/after 7am
            ## Reset Count
            #print("Loading last saved count.")
            date1 = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            rack_count = 0
            pallette_count = 0
            print("Counts were reset")
            with open("Count_backup/saved_rack_count.txt", "w") as f:
                f.write(str(rack_count) +"#"+ date1)

            # with open("Count_backup/saved_palette_count.txt", "w") as f:
            #     f.write(str(palette_count) +"#"+ date1)
            break
        else:
            print("Counts were Reloaded")
            rack_count = int(r)
            ### Not Implemeted
            palette_count = int(0)
    else:
        print("Shutdown has happened for more than a day reseting counts...")
        rack_count = 0
        palette_count = 0
            

while(cap.isOpened()): 
    # Capture frames in the video 
    ret, frame = cap.read() 
    #if(frame == None):
    #    print("OOOOps")
    #    break
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
         
    elif( p1<0.15):
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
    else:
        cv2.putText(frame,  
            'Dead Zone {}'.format(p1),  
            (100, 100),  
            font, 0.5,  
            (0, 255, 255),  
            2,  
            cv2.LINE_4)
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
        print("Update local files")
        updateHistory(out_dict)
        produceDataPdf()
        hourlyLogInit()
        ### Reinstantiate Output Dictionary
        out_dict  = {
            'Start Date and Time': [],
            'End Date and Time':[],
            'Total Rack Count':[],
            'Total Palette Count':[]
            }

        ### Update Firebase Database with daily summary
        print("Attempting to update Firebase Database")
        try:
            # bucket = storage.bucket()
            # blob = bucket.blob("LPU/lpuHistory.pdf")
            # blob.upload_from_filename("lpuHistory.pdf")
            doc_ref = db.collection(u'counts_log').document(
                datetime.datetime.now().strftime("%Y-%m-%d"))
            doc_ref.set({
                u'dateTime': datetime.datetime.now(),
                u'totalRackCount': '{}'.format(rack_count),
                u'totalPaletteCount': '{}'.format(palette_count),
                u'id': '{}'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
                })
            bucket = storage.bucket()
            blob = bucket.blob("LPU/LPU_daily_counts.csv")
            blob.upload_from_filename("logs/LPU_daily_counts.csv")
        except:
            print("Error Connecting to Firebase")
            print("Attemting to reconnect to Firebase Database")
            try:
                ### Reinitialise fibase app
                print("Connecting.... ")
                print("Authenticating and Reinitializing Firebase App")
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    'storageBucket': bucket_path
                    })
                db = firestore.client()
            except:
                print("Problem persists Moving on")      
         
        ### Reset start daily time
        count_start_time = count_start_time + daily_delta
        daily_reset_flag = True
        print("..............Finished.............")
        rack_count = 0
        palette_count = 0
        with open(os.getcwd() +"/Count_backup/saved_rack_count.txt", "w") as f:
           f.write(str(rack_count) +"#"+ datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        # with open("Count_backup/saved_palette_count.txt", "w") as f:
        #     f.write(str(palette_count) +"#"+ datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    ### Reset daily reset flag
    if(time.localtime(time.time()).tm_mday == 1):
        daily_reset_flag = False
 
    ### hourly udate
    if(time.localtime(time.time()).tm_hour != hour_index_check ):
        hour_index_check = hour_index_check + 1
        date = datetime.datetime.now().strftime("%y_%m_%d")
        datetime1 = datetime.datetime.now().strftime("%y-%m-%d-%H")
        # data_fileName = "lpuHistory.pdf"
        data_filename = "logs/"+date+"_hourly_count.csv"
        outh = {"dateTime":[datetime1],
            "hourlyPaletteCount": [0], 
            "hourlyRackCount": [rack_count]}
        updateHourlyHistory(outh)
        #####################################################
        ### Updating firbase storage and Firestare
        try:
            print("Updating Hourly Log")
            # bucket = storage.bucket()
            # blob = bucket.blob("LPU/"+ data_fileName)
            # blob.upload_from_filename(data_fileName)
            doc_ref = db.collection(u'counts_hourly').document(
                "hour_{}".format(time.localtime(time.time()).tm_hour))
            doc_ref.set({
                u'dateTime': datetime.datetime.now(),
                u'hourlyRackCount': '{}'.format(rack_count),
                u'hourlyPaletteCount': '{}'.format(palette_count),
                u'id': "hour_{}".format(time.localtime(time.time()).tm_hour)
                })
            bucket = storage.bucket()
            blob = bucket.blob("LPU/" + data_filename)
            blob.upload_from_filename(os.getcwd()+'/' +data_filename)
            blob1 = bucket.blob("LPU/LPU_hourly_counts.csv")
            blob1.upload_from_filename(os.getcwd() + '/'+data_filename)
        except:
            print("Error Connecting to Firebase")
            print("Attemting to reconnect to Firebase Database")
            try:
                ### Reinitialise fibase app
                print("Connecting.... ")
                print("Authenticating and Reinitializing Firebase App")
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    'storageBucket': bucket_path
                    })
                db = firestore.client()
            except:
                print("Problem Persists Moving On")      
        #################################################
        ### Reset start daily time
        count_start_time = count_start_time + daily_delta
        daily_reset_flag = True
        print("..............Finished.............")
  

    ### Minute Count Update
    if((datetime.datetime.now()-count_update_minute_start)>minute_delta):
        print("Updating count.........")
        print("Rack Count:",rack_count)
        print("Palette Count: Not implemeted")
        print("Saving Count Value locally")

        with open(os.getcwd()+'/'+"Count_backup/saved_rack_count.txt", "w") as f:
           f.write(str(rack_count) +"#"+ datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        # with open("Count_backup/saved_palette_count.txt", "w") as f:
        #     f.write(str(palette_count) +"#"+ datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        print("Attempting to update online count... ")
        try:
            doc_ref = db.collection(u'counts_live').document(u'lpu_counts')
            doc_ref.set({
                u'count_reset': '{}'.format(datetime.datetime.now().strftime("%H:%M")),
                u'rack_count': '{}'.format(rack_count),
                u'palette_count': '{}'.format(palette_count),
                u'id':'lpu_counts'
                })
        except:
            print("Error Connecting to Firebase")
            print("Attemting to reconnect to Firebase Database")
            try:
                ### Reinitialise fibase app
                print("Connecting.... ")
                print("Authenticating and Reinitializing Firebase App")
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    'storageBucket': bucket_path
                    })
                db = firestore.client()
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