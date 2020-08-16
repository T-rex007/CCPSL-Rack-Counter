#import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("IP", help = "Ip address of camera", type = str)
args = parser.parse_args()



#model = tf.saved_model.load('APLU_Sequential_Model.model')
cap = cv2.VideoCapture(0)
print(args.IP)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Pre-processing
    ### If frame is not empty perform preprocessing
    if(ret== True): 
        img = frame/255.0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()