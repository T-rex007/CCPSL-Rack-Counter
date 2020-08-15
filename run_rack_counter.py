import numpy as np
import cv2 
import argparse
import time
import datetime
from helper import *
from tensorflow.keras.models import model_from_json

### Command Line Arguments 
parser = argparse.ArgumentParser()
parser.add_argument("IP", help = "Ip address of camera", type = str)
args = parser.parse_args()

### Load Model
json_file = open('Models/smally_rack_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("Models/smally_rack_model.h5")
print("Loaded model from disk")

### Predefined Region
r1 = (150, 368, 63, 41)
### Address to video stream
ip = 'Videos/rack.mp4'
### Vdeo streaming Object
cap = cv2.VideoCapture(ip) 


isRegionSelected = 1
rack_count = 0
palette_count = 0
p1_change = False
font = cv2.FONT_HERSHEY_SIMPLEX

out_dict  = {'Start Date and Time': [],
             'End Date and Time':[],
             'Total Rack Count':[],
            'Total Palette Count':[]} 
while(True): 
      
    # Capture frames in the video 
    ret, frame = cap.read() 
    frame1 = cv2.cvtColor(np.copy(frame), cv2.COLOR_BGR2RGB)
    if (isRegionSelected == 0):
        # Select ROI
        r1 = cv2.selectROI(frame)
        # Crop image
        imCrop1 = frame1[int(r1[1]):int(r1[1]+r1[3]), int(r1[0]):int(r1[0]+r1[2])]
        imCrop2 = frame1[int(r2[1]):int(r2[1]+r2[3]), int(r2[0]):int(r2[0]+r2[2])]
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
    
    if((datetime.datetime.now()-start)>datetime.timedelta(hours = 1)):
        out_dict['Start Date and Time'].append(
            datetime.datetime.now() - datetime.timedelta(days = 1))
        out_dict['End Date and Time'].append(datetime.datetime.now())
        out_dict['Total Rack Count'].append(rack_count)
        out_dict['Total Palette Count'].append(palette_count)### Not implemted
        updateHistory(output_dict)

        ### Reinstantiate Output Dictionary
        out_dict  = {
            'Start Date and Time': [],
            'End Date and Time':[],
            'Total Rack Count':[],
            'Total Palette Count':[]
            }
        updateHistory()
        print("Reseting LPU System .....")
    # Display the resulting frame 
    cv2.imshow('video', frame) 

    # Set 'q' as the quit  
    # button for the video 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# release the cap object 
cap.release() 
# close all windows 
cv2.destroyAllWindows() 