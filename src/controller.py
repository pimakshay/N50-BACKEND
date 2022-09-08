import pandas as pd
import os
from sklearn import preprocessing
from collections import deque

class DataHandler:

    def __init__(self) -> None:
        
        pass

    def read_csv(col_names, filenames):
        '''
            This function reads all the text files and stores the data in dataframes.
            Args:
            :col_names: column names of the individual data files
            :filenames: name of files (companies) for the given data
        '''
        main_df = pd.DataFrame(columns=col_names)
        # l = [pd.read_csv(filename, names=col_names) for filename in glob.glob("data/nifty50/05SEPsample/*.txt")
        #         if filename[0]]
        # df = pd.concat(l, axis=0)
        for filename in filenames:
                df = pd.read_csv(filename, names=col_names)
                basename = os.path.basename(filename) #gives companyname.txt
                bs1,bs2 = basename.split('.') # splits the string

                # rename close and volume columns; and remove other columns from df
                df.rename(columns={"close":f"{bs1}_close", "volume":f"{bs1}_volume"}, inplace=True)
                df.set_index("time",inplace=True)
                df = df[[f"{bs1}_close",f"{bs1}_volume"]]

                if len(main_df) == 0:
                        main_df = df
                else:
                        main_df = main_df.join(df)

        return main_df

    def preprocess_df(df, SEQ_LEN):
        #task 1: scaling
        df = df.drop('future', 1)

        for col in df.columns:
            if col != "target":
                df[col] = df[col].pct_change() # Percentage change between the current and a prior element.
                df.dropna(inplace=True)
                
                # try:
                #     df[col] = preprocessing.scale(df[col].values) #scaling the data to 0 to 1
                # except ValueError:
                #     print("column name: ", col)
                df[col] = preprocessing.scale(df[col].values)
        df.dropna(inplace=True)
        sequential_data = []

        prev_days = deque(maxlen=SEQ_LEN)     

        print(df.head())

        for c in df.columns:
            print(c)
        # for i in df.values():
        #     pass


class Model:

    def __init__(self) -> None:
          pass

    def classify(current, future):
        '''
            :TODO: change the buying/selling strategy, 
                buy if future > x * current! x>1.0 (ex: aleast 10percent higher, then x=1.1) 
        '''
        if float(future) > float(current):
            return 1 #sell
        else:
            return 0 #buy
