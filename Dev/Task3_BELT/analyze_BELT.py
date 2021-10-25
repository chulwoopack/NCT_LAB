import os
import pandas as pd
import numpy as np
import argparse

'''
Parse Arguments
'''
parser = argparse.ArgumentParser(description='Analyze BELT')
parser.add_argument('-csv_path', type=str, required=True,
                   help='a path to the CSV file (e.g., PARTICIPANTID_BELT_TEST_YYYY_MMM_DD_XXXX.csv')
parser.add_argument('-log_path', type=str, required=True,
                   help='a path to the log file (e.g., PARTICIPANTID_BELT_TEST_YYYY_MMM_DD_XXXX.log')
args = parser.parse_args()

CSV_PATH = args.csv_path   # './data/AA06LC00_BELT_TEST_2021_Jun_09_1320.csv'
LOG_PATH  = args.log_path  # './data/AA06LC00_BELT_TEST_2021_Jun_09_1320.log'
print("[INFO] Processing {}...".format(CSV_PATH))
subject_id = os.path.basename(CSV_PATH).split('_')[0]

'''
Class BELT_Analyzer:
    The main purpose of this class is to store dataframe of csv and log file.
    Various functions to compute response time and poppedness of balloons are also included.
'''
class BELT_Analyzer:
    def __init__(self, main_csv_path, log_path):
        self.main_csv_path = main_csv_path
        self.log_path      = log_path
        
        self.data_main     = pd.read_csv(self.main_csv_path)
        self.data_log      = self.readLog(self.log_path)
        self.data_main_ext = self.setResponseTimeOnMainFromLog(self.data_log)
    
    '''
    computeResTime:
        Get an array containing a sequence of timestamp.
        Return an array containing the time differences.
        e.g.) input <- [1,4,12,13]
              output <- [3,8,1]
    '''
    def computeResTime(self, timelist):
        diff = timelist[1:] - timelist[:-1]
        return diff
    
    
    '''
    getBalloonPointsAndPops:

    '''
    def getBalloonPointsAndPops(self, dataframe):
        # blueballoon
        blueballoon_points = np.sum(dataframe[dataframe['imgroot']=='blueballoon']['balloonscore'].values)
        blueballoon_pops   = len(np.argwhere(dataframe[dataframe['imgroot']=='blueballoon']['balloonscore'].values==0))
        # pinkballoon
        pinkballoon_points = np.sum(dataframe[dataframe['imgroot']=='pinkballoon']['balloonscore'].values)
        pinkballoon_pops   = len(np.argwhere(dataframe[dataframe['imgroot']=='pinkballoon']['balloonscore'].values==0))
        # orangeballoon
        orangeballoon_points = np.sum(dataframe[dataframe['imgroot']=='orangeballoon']['balloonscore'].values)
        orangeballoon_pops   = len(np.argwhere(dataframe[dataframe['imgroot']=='orangeballoon']['balloonscore'].values==0))
        result = {"blue_score"  : [blueballoon_points],
                  "blue_pops"   : [blueballoon_pops],
                  "pink_score"  : [pinkballoon_points],
                  "pink_pops"   : [pinkballoon_pops],
                  "orange_score": [orangeballoon_points],
                  "orange_pops" : [orangeballoon_pops]}
        return result
    
    '''
    readLog:
    '''
    def readLog(self,log_path):
        # Read .log file and store data into dataframe
        with open(log_path, mode='r', encoding='UTF-8') as f:
            time_list = []
            type_list = []
            mesg_list = []
            for line in f:
                columns = line.split("\t")
                time_list.append(float(columns[0].rstrip()))
                type_list.append(columns[1].rstrip())
                mesg_list.append(columns[2].rstrip())
        data_json = {'timestamp':time_list, 'datatype':type_list, 'msg':mesg_list}
        data_log = pd.DataFrame(data_json)
        return data_log
    
    '''
    setResponseTimeFromLog:

    '''
    def setResponseTimeOnMainFromLog(self, data_log):
        # This list will contain the average reaction(response) time of each trial (balloon)
        out_avg_rxn_time = []
        
        _timestamp = []
        # Iterate log data, for each new trial, collect timestamp when a participant hit a button.
        for index, row in data_log.iterrows():
            # New balloon is shown. Empty timestamp buffer.
            if row['msg'].startswith('New trial'):
                # Corner case: Very first trial of experiment.
                if(len(_timestamp)==0):
                    pass
                else:
                    _restime_arr = self.computeResTime(np.array(_timestamp))
                    #print("Score: {} Avg_rxn_time: {}".format(len(_restime_arr), np.mean(_restime_arr)))
                    out_avg_rxn_time.append(np.mean(_restime_arr))
                    _timestamp = []
                _timestamp.append(row['timestamp'])
            if row['msg'].startswith('Keypress: space'):
                _timestamp.append(row['timestamp'])
        _restime_arr = self.computeResTime(np.array(_timestamp[:-1]))
        #print("Score: {} Avg_rxn_time: {}".format(len(_restime_arr), np.mean(_restime_arr)))
        out_avg_rxn_time.append(np.mean(_restime_arr))

        self.data_main["avgRxnTime"] = out_avg_rxn_time
        
'''
main driver
'''
my_BELT = BELT_Analyzer(CSV_PATH, LOG_PATH)

# Task 1: points on balloons by color (condition)
save_path = subject_id+"_balloonscore_per_color.csv"
pd.DataFrame(my_BELT.data_main.groupby('imgroot').mean().balloonscore).to_csv(save_path)
print("[INFO] Output is saved at {}".format(save_path))

# Task 2: number of points for each participant
save_path = subject_id+"_balloonscore_pop.csv"
total_balloonscore = np.sum(my_BELT.data_main['balloonscore'].values)

# Task 3: number of pops per participant*
total_pops = len(np.argwhere(my_BELT.data_main['balloonscore'].values==0))
pd.DataFrame({"total_balloonscore":[total_balloonscore],"total_pops":[total_pops]}).to_csv(save_path,index=False)
print("[INFO] Output is saved at {}".format(save_path))

# Task 4: number of pops and number of points per color condition overall*
## first half
save_path = subject_id+"_balloonscore_pop_per_color_first_half.csv"
data_main_first_half = my_BELT.data_main[my_BELT.data_main['trials.thisRepN']==0]
pd.DataFrame(my_BELT.getBalloonPointsAndPops(data_main_first_half)).to_csv(save_path,index=False)
print("[INFO] Output is saved at {}".format(save_path))
## second half
save_path = subject_id+"_balloonscore_pop_per_color_second_half.csv"
data_main_second_half = my_BELT.data_main[my_BELT.data_main['trials.thisRepN']==1]
pd.DataFrame(my_BELT.getBalloonPointsAndPops(data_main_second_half)).to_csv(save_path,index=False)
print("[INFO] Output is saved at {}".format(save_path))

# Task 5: average reaction time after popped balloons*
save_path = subject_id+"_avg_rxntime_after_popped.csv"
popped_balloons_trial_idx = np.argwhere(my_BELT.data_main['balloonscore'].values==0).squeeze()
if(len(popped_balloons_trial_idx)<1):
    print("[WARN] No popped balloons")
else:
    popped_balloons_trial_idx += 1 # increase index to target the AFTER popped
    # The last balloon is popped. In this case, there is no more following trial to compute, thus we ignore the last pop.
    if(popped_balloons_trial_idx[-1]==len(my_BELT.data_main)-1):
        print("[WARN] A balloon is poppped at the last trial. Thus, unable to compute avg reaction time AFTER popped balloon.")
        popped_balloons_trial_idx = popped_balloons_trial_idx[:-1]
    avg_rxntime_after_popped = np.mean(my_BELT.data_main.iloc[np.argwhere(my_BELT.data_main['balloonscore'].values==0).squeeze() + 1].avgRxnTime)
pd.DataFrame({"avg_rxntime_after_popped":[avg_rxntime_after_popped]}).to_csv(save_path,index=False)
print("[INFO] Output is saved at {}".format(save_path))

# Task 6: average reaction time by color
save_path = subject_id+"_avg_rxntime_by_color.csv"
pd.DataFrame(my_BELT.data_main.groupby('imgroot').mean().avgRxnTime).to_csv(save_path,index=False)
print("[INFO] Output is saved at {}".format(save_path))

# Task 7: split blue balloons into load sizes (there are three) with average reaction time for each
save_path = subject_id+"_avg_rxntime_by_loadsize.csv"
pd.DataFrame(my_BELT.data_main[my_BELT.data_main['imgroot']=='blueballoon'].groupby('maxpumps').mean().avgRxnTime).to_csv(save_path)
print("[INFO] Output is saved at {}".format(save_path))

print("[INFO] Completed.")
