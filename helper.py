import pandas as pd
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tensorflow.keras.models import model_from_json
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages



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
        report: Dictionary with the pre-specified format of count_log.csv
            (Same header names) 
    """
    df_new = pd.DataFrame(report)
    df1 = pd.read_csv("count_log.csv",index_col =  False)
    df = df1.append(df_new, ignore_index = True
          )
    df.to_csv("count_log.csv", index = False)

def produceDataPdf(df):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot()
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
    pp = PdfPages("lpuHistory.pdf")
    pp.savefig(fig, bbox_inches='tight', dpi = 5)
    pp.close()

