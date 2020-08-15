
### Predefined Region
r1 = (150, 368, 63, 41)

### Address to video stream
ip = 'Videos/rack.mp4'
### Vdeo streaming Object
cap = cv2.VideoCapture(ip) 
isRegionSelected = 1
count = 0
p1_change = False
font = cv2.FONT_HERSHEY_SIMPLEX 
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
            count = count +1
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
                'Racks counted {}'. format(count),  
                (170, 170),  
                font, 0.5,  
                (0, 255, 255),  
                2,  
                cv2.LINE_4)
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