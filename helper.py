import pandas as pd
import numpy as np
import cv2
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tensorflow.keras.models import model_from_json
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Activation, MaxPooling2D, Dropout


def cropAndPredict(frame1, r1, loaded_model):
    imCrop1 = frame1[int(r1[1]):int(r1[1]+r1[3]), int(r1[0]):int(r1[0]+r1[2])]
    img1 = np.copy(imCrop1)
    img1 = np.expand_dims(cv2.resize(img1/255.0, (64,64)), axis = 0) 
    ### Model Prediction
    p1 = loaded_model.predict(img1)
    return p1

def updateHistory(report):
    """
    Args:
        Report: Dictionary with the pre-specified format of count_log.csv
            (Same header names) 
    """
    df_new = pd.DataFrame(report)
    df1 = pd.read_csv("logs/count_log.csv",index_col =  False)
    df = df1.append(df_new, ignore_index = True
          )
    df.to_csv("logs/count_log.csv", index = False)

def produceDataPdf(df):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot()
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
    pp = PdfPages("logs/lpuHistory.pdf")
    pp.savefig(fig, bbox_inches='tight', dpi = 5)
    pp.close()

def RackNet():
    ### CREATE SEQUENTIAL MODEL
    input_shape = (64, 64, 3)
    print (input_shape)
    print('Creating Model')
    model = Sequential()
    #filters,kernel_size,strides=(1, 1),padding='valid',data_format=None,dilation_rate=(1, 1),activation=None,use_bias=True,
    #kernel_initializer='glorot_uniform',bias_initializer='zeros',kernel_regularizer=None,bias_regularizer=None,
    #activity_regularizer=None,kernel_constraint=None,bias_constraint=None,
    #pool_size=(2, 2), strides=None, padding='valid',data_format=None
    model.add(Conv2D(32, (3,3),padding='same',input_shape=input_shape,name='conv2d_1'))
    model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2),name='maxpool2d_1'))
    model.add(Conv2D(64, 3, 3, name='conv2d_6'))
    model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(32))
    #model.add(Dropout(0.5))
    model.add(Dense(1)) #config.num_classes
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                optimizer='Adam',
                metrics=['accuracy'])
    return model

