import os
import pandas as pd
import numpy as np
import argparse

# Ver. 1 (5/5/2022)

'''
Parse Arguments
'''
parser = argparse.ArgumentParser(description='Analyze Face-matching Task')
parser.add_argument('-csv_path', type=str, required=True,
                   help='a path to the main CSV file (e.g., BANDAXXX_Scanner_AB_FaceMatching_XXX_XXX_XX_XXXX.csv')
args = parser.parse_args()

CSV_PATH = args.csv_path
print("[INFO] Processing {}...".format(CSV_PATH))

# Read data
face_data = pd.read_csv(CSV_PATH)
if(len(face_data.columns)<=1):
    face_data = pd.read_csv(CSV_PATH, sep='\t')

''' Part 1: Get (1) average response time and (2) Number of correct response per condition '''
df_groupby = face_data.groupby(by=['Condition'])
data_columns     = ['Condition', 'Avg Response Time', 'Num of Correct Resp']
data_conditions  = list(df_groupby.groups.keys()) #+ ['Correct Resp','Incorrect Resp']
# average response times per condition (found in R (i.e., key_resp_trial.rt))
data_avgResTimes = list(df_groupby['key_resp_trial.rt'].mean().values)
# number correct per condition (correct responses in Q (i.e., key_resp_trial.corr))
data_cntCorr     = list(df_groupby['key_resp_trial.corr'].sum().astype(int).values)

''' Part 2: Get average response time for correct and incorrect response '''
# average response time for correct (found in R (i.e., key_resp_trial.rt))
_data_avgRespTimeForCorr   = face_data[face_data['key_resp_trial.corr']==1]['key_resp_trial.rt'].mean()
# average response time for incorrect (found in R (i.e., key_resp_trial.rt))
_data_avgRespTimeForIncorr = face_data[face_data['key_resp_trial.corr']==0]['key_resp_trial.rt'].mean()

''' Part 1 and 2 ''' 
data_conditions += ['-','Corr Resp','Incorr Resp']
data_avgResTimes += ['-',_data_avgRespTimeForCorr,_data_avgRespTimeForIncorr]
data_cntCorr     += ['-','-','-']

data_out     = np.array([data_conditions,data_avgResTimes,data_cntCorr]).transpose()
df_data_out  = pd.DataFrame(data=data_out, columns=data_columns)

save_filename = 'analyzed_' + os.path.splitext(os.path.basename(CSV_PATH))[0] + '.csv'
df_data_out.to_csv(save_filename, index=False)
print("[INFO] Output is saved as {}".format(save_filename))