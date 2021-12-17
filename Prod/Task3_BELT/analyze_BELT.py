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
        self.setResponseTimeOnMainFromLog(self.data_log)
    
    '''
    computeResTime:
        Get an array containing a sequence of timestamp.
        Return an array containing the time differences.
        e.g.) input <- [1,4,12,13]
              output <- [3,8,1]
    '''
    def computeResTime(self, timelist):
        if(len(timelist)<2):
            return [np.nan]
        else:
            diff = timelist[1:] - timelist[:-1]
            return diff
    
    '''
    computeResTimeOnset:
        Get an array containing a sequence of timestamp.
        Return the first reaction time after a ballon is presented.
        e.g.) input <- [1,4,12,13]
              output <- 3 (i.e., 4-1)
    '''
    def computeResTimeOnset(self, timelist):
        if(len(timelist)<2):
            return np.nan
        else:
            return timelist[1]-timelist[0]
        
    '''
    computeTrialDuration:
        Get an array containing a sequence of timestamp.
        Return the duration of timestamp.
        e.g.) input <- [1,4,12,13]
              output <- 12 (i.e., 13-1)
    '''
    def computeTrialDuration(self, timelist):
        if(len(timelist)<2):
            return 0.0
        else:
            return timelist[-1]-timelist[0]

    
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
                try:
                    columns = line.split("\t")
                    time_list.append(float(columns[0].rstrip()))
                    type_list.append(columns[1].rstrip())
                    mesg_list.append(columns[2].rstrip())
                except ValueError:
                    continue
        data_json = {'timestamp':time_list, 'datatype':type_list, 'msg':mesg_list}
        data_log = pd.DataFrame(data_json)
        return data_log
    
    '''
    setResponseTimeFromLog:

    '''
    def setResponseTimeOnMainFromLog(self, data_log):
        # This list will contain the timestamp of the participant's action (for detailed analysis)
        action_timestamp = []
        
        # This list will contain the average reaction time per presentation from onset stimulus
        onset_avg_rxn_time = []
        
        # This list will contain the average reaction time from previous stimulus
        prev_avg_rxn_time = []
        _prev_stimulus_time = 0
        _curr_rxn_time = 0
         
        # This list will contain the average reaction(response) time of each trial (balloon)
        out_avg_rxn_time = []
        
        _timestamp = []
        
        # This list will contain the average reaction(response) time of each trial (balloon)
        out_avg_rxn_time = []
        
        # This list will contain the trial duration
        trial_duration = []
        
        # A flag to filter and skip unexpected "Keypress: space" before the very first "New trial"
        _flag_first_new_trial = True
        
        # A flag for indicating the end of trial (based on "popped" or "score")
        trial_end_keywords = ['Popped', 'Score']
        _flag_trialend = False
        
        # Iterate log data, for each new trial, collect timestamp when a participant hit a button.
        for index, row in data_log.iterrows():
            # New balloon is shown. Empty timestamp buffer.
            if row['msg'].startswith('New trial'):
                _flag_trialend = False
                # Corner case: Very first trial of experiment.
                if(len(_timestamp)==0):
                    _flag_first_new_trial = False
                    pass
                else:
                    action_timestamp.append(_timestamp)
                    onset_avg_rxn_time.append(self.computeResTimeOnset(np.array(_timestamp)))
                    _restime_arr = self.computeResTime(np.array(_timestamp))
                    #print("Score: {} Avg_rxn_time: {}".format(len(_restime_arr), np.mean(_restime_arr)))
                    out_avg_rxn_time.append(np.mean(_restime_arr))
                    
                    _timestamp = []
                _timestamp.append(row['timestamp'])
            if _flag_first_new_trial==False:
                if(any(keyword in row['msg'] for keyword in trial_end_keywords)):
                    _flag_trialend = True
                elif(_flag_trialend==False and row['msg'].startswith('Keypress: space')):
                    _timestamp.append(row['timestamp'])
                elif(_flag_trialend==False and row['msg'].startswith('Keypress: return')):
                    _timestamp.append(row['timestamp'])
                else:
                    continue
            
                
        action_timestamp.append(_timestamp)
                
        onset_avg_rxn_time.append(self.computeResTimeOnset(np.array(_timestamp)))
        _restime_arr = self.computeResTime(np.array(_timestamp[:-1]))
        #print("Score: {} Avg_rxn_time: {}".format(len(_restime_arr), np.mean(_restime_arr)))
        out_avg_rxn_time.append(np.mean(_restime_arr))

        # corner-case: last timestamp of the first trial - first timestamp of the first trial
        prev_avg_rxn_time_first_trial = self.computeTrialDuration(action_timestamp[0])
        prev_avg_rxn_time.append(prev_avg_rxn_time_first_trial)  
        prev_avg_rxn_time += self.computeResTime(np.array([i[0] for i in action_timestamp])).tolist()
        
        # compute trial duration (note: if there is only one timestamp for a trial, put 0.0)
        for i in action_timestamp:
            _trialDuration = self.computeTrialDuration(np.array(i))
            trial_duration.append(_trialDuration)
        
        # All detailed timestamp (for logging purpose)
        self.data_main['timestamps'] = action_timestamp
        # Average reaction time per presentation from onset stimulus
        self.data_main["avgOnsetRxnTime"] = onset_avg_rxn_time
        # Average reaction time from previous stimulus
        self.data_main["avgPrevRxnTime"]  = prev_avg_rxn_time
        # Average reaction(response) time of each trial (balloon)
        self.data_main["avgRxnTime"] = out_avg_rxn_time
        # Trial duration
        self.data_main["trialDuration"] = trial_duration
  
        
'''
main driver
'''
my_BELT = BELT_Analyzer(CSV_PATH, LOG_PATH)

# Task 1: response time per presentation from onset stimulus
# Task 2: response time from previous stimulus
save_path = subject_id+"_rxntime_from_onset_from_previous.csv"
my_BELT.data_main.to_csv(save_path)
print("[INFO] Output is saved at {}".format(save_path))

##################################################
# Stats from task 3 to task 9 will be aggregated #
##################################################
# This list will collect all computed data
save_path = subject_id+"_aggregated_stats.csv"
aggregate_data = []

# Task 3: points on balloons by color (condition)
prefix = "balloonscore_per_color"
for key,value in my_BELT.data_main.groupby('imgroot').mean().balloonscore.to_dict().items():
    _data = (prefix, key, value)
    aggregate_data.append(_data)

# Task 4: number of points for each participant
total_balloonscore = np.sum(my_BELT.data_main['balloonscore'].values)
prefix = "balloonscore_pop"
_data = (prefix, "total_balloonscore", total_balloonscore)
aggregate_data.append(_data)

# Task 5: number of pops per participant*
total_pops = len(np.argwhere(my_BELT.data_main['balloonscore'].values==0))
_data = (prefix, "total_pops", total_pops)
aggregate_data.append(_data)

# Task 6: number of pops and number of points per color condition overall*
data_len = len(my_BELT.data_main)
if(data_len!=54):
    print("[WARN] The number of data entry is not divisibly by 3 ({}/3).".format(len(my_BELT.data_main)))
else:
    data_main_first_part  = my_BELT.data_main[:data_len//3]
    data_main_second_part = my_BELT.data_main[data_len//3:data_len//3*2]
    data_main_third_part  = my_BELT.data_main[data_len//3*2:]
prefix = "balloonscore_pop_per_color_first_third"
for key,value in my_BELT.getBalloonPointsAndPops(data_main_first_part).items():
    _data = (prefix, key, value[0])
    aggregate_data.append(_data)
prefix = "balloonscore_pop_per_color_second_third"
for key,value in my_BELT.getBalloonPointsAndPops(data_main_second_part).items():
    _data = (prefix, key, value[0])
    aggregate_data.append(_data)
prefix = "balloonscore_pop_per_color_last_third"
for key,value in my_BELT.getBalloonPointsAndPops(data_main_third_part).items():
    _data = (prefix, key, value[0])
    aggregate_data.append(_data)
    
# Task 7: average reaction time after popped balloons*
popped_balloons_trial_idx = np.argwhere(my_BELT.data_main['balloonscore'].values==0).squeeze()
if(len(popped_balloons_trial_idx)<1):
    print("[WARN] No popped balloons")
else:
    popped_balloons_trial_idx += 1 # increase index to target the AFTER popped
    # The last balloon is popped. In this case, there is no more following trial to compute, thus we ignore the last pop.
    if(popped_balloons_trial_idx[-1]==len(my_BELT.data_main)):
        print("[WARN] A balloon is poppped at the last trial. Thus, the corresponding reaction time is not reflected to the calculation.")
        popped_balloons_trial_idx = popped_balloons_trial_idx[:-1]
    avg_rxntime_after_popped = np.mean(my_BELT.data_main.iloc[popped_balloons_trial_idx]).avgRxnTime
prefix = "avg_rxntime_after_popped"
_data = (prefix, "avg_rxntime_after_popped", avg_rxntime_after_popped)
aggregate_data.append(_data)

# Task 8: average reaction time by color
prefix = "avg_rxntime_by_color"
for key,value in pd.DataFrame(my_BELT.data_main.groupby('imgroot').mean().avgRxnTime).to_dict()['avgRxnTime'].items():
    _data = (prefix, key, value)
    aggregate_data.append(_data)

# Task 9: split blue balloons into load sizes (there are three) with average reaction time for each
prefix = "avg_rxntime_by_loadsize"
for key,value in pd.DataFrame(my_BELT.data_main[my_BELT.data_main['imgroot']=='blueballoon'].groupby('maxpumps').mean().avgRxnTime).to_dict()['avgRxnTime'].items():
    _data = (prefix, key, value)
    aggregate_data.append(_data)
pd.DataFrame(aggregate_data, columns=['Task','Key','Value']).to_csv(save_path,index=False)
print("[INFO] Output is saved at {}".format(save_path))

# Task 10: post_explosion_behavior - Collect every popped case, and the right after the same condition.
save_path = subject_id+"_post_explosion_behavior.csv"
my_BELT.data_main['local_index'] = my_BELT.data_main.index
df_post_explosion_behavior = my_BELT.data_main.sort_values(by=['imgroot','local_index']).reset_index(drop=True)
post_explosion_behavior_data =[]
for index, row in df_post_explosion_behavior.iterrows():
    # 1. Find the exploded case
    if row['balloonscore']==0:
        post_explosion_behavior_data.append(tuple(row))
        # 2.1 Ignore the exploded case at the last trial
        if(index<data_len-1):
            # 2.2 Ignore the explosion right after the explosion 
            if(df_post_explosion_behavior.iloc[index+1]['balloonscore']==0):
                continue
            # 2.3. Make sure the post behavior is for the same condition
            if(df_post_explosion_behavior.iloc[index]['imgroot']==df_post_explosion_behavior.iloc[index+1]['imgroot']):
                post_explosion_behavior_data.append(tuple(df_post_explosion_behavior.iloc[index+1]))
pd.DataFrame(post_explosion_behavior_data, columns=df_post_explosion_behavior.columns.to_list()).to_csv(save_path,index=False)
print("[INFO] Output is saved at {}".format(save_path))

print("[INFO] Completed.")
