
import pandas as pd

def preprocess(img):
    output_img = 0
    return output_img

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