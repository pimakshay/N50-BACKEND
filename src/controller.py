import pandas as pd
import os

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