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

### FireBase Authentication
credential_path = "/home/trex/workspace/liveplant_updates/rack_detector/Auth/ccpsl-1797d-firebase-adminsdk-333t0-02b1f5b581.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
### Initializing Firebase App
default_app = firebase_admin.initialize_app()
db = firestore.client()

### Command Line Arguments 
parser = argparse.ArgumentParser()
parser.add_argument("IP", help = "Ip address of camera", type = str)
parser.add_argument("SupressDisplay", help = "Whether or not to suppress the display", type = bool)
args = parser.parse_args()

### Load Model
json_file = open('Models/smally_rack_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("Models/smally_rack_model.h5")
print("Loaded model from disk")

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

count_start_time = datetime.datetime.now()
count_update_minute_start = datetime.datetime.now()
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
        #imCrop2 = frame1[int(r2[1]):int(r2[1]+r2[3]), int(r2[0]):int(r2[0]+r2[2])]
        #############################################################################
        
        # Crop image
        isRegionSelected = 1

    ### Preprocessing
    imCrop1 = frame1[int(r1[1]):int(r1[1]+r1[3]), int(r1[0]):int(r1[0]+r1[2])]
    frame = cv2.rectangle(frame,
                          (int(r1[0]),int(r1[1])),
                          (int(r1[0] +r1[2]),int(r1[1]+r1[3])),
                          (255, 0, 0), 2
                         )
    img1 = np.copy(imCrop1)
    img1 = np.expand_dims(cv2.resize(img1/255.0, (64,64)), axis = 0)
    
    ### Model Prediction
    p1 = loaded_model.predict(img1)
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
    if((datetime.datetime.now()-count_start_time)>daily_delta):
        print("Reseting LPU System .....")
        out_dict['Start Date and Time'].append(
            datetime.datetime.now() - datetime.timedelta(days = 1))
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
        count_start_time = datetime.datetime.now()

    ### Count update
    if((datetime.datetime.now()-count_update_minute_start)>minute_delta):
        doc_ref = db.collection(u'counts').document(u'lpu_counts')
        doc_ref.set({
            u'count_reset': 'hour:minute' ,
            u'rack_count': 'kevin_is_more_shit_shittier_than_shit',
            u'palette_count': 'Anjana_is_shit'
            })
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