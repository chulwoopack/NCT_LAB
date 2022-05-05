import os
import pandas as pd
import numpy as np
import argparse

# Ver. 1 (5/5/2022)

'''
Parse Arguments
'''
parser = argparse.ArgumentParser(description='Analyze BANDA')
parser.add_argument('-csv_path', type=str, required=True,
                   help='a path to the main CSV file (e.g., BANDAXXX_Scanner_ABCD_conflict_XXXX_XXX_XX_XXXX.csv')
args = parser.parse_args()

CSV_PATH = args.csv_path
print("[INFO] Processing {}...".format(CSV_PATH))

# Read data
conflict_data = pd.read_csv(CSV_PATH, keep_default_na=False, na_values=[np.NaN])
if(len(conflict_data.columns)<=1):
    conflict_data = pd.read_csv(CSV_PATH, keep_default_na=False, na_values=[np.NaN], sep='\t')

'''
1. Use column A/K to define condition.
    - Column A: facesAreFearful (0 or 1)
    - Column K: facesAreAttended (0 or 1)
    - Thus, a total of 4 possible conditions

2. Use column T for response time.
    - Column T: SameDiffResponse.rt
    
3. Use column S compared to H
    - Column S: SameDiffResponse.keys
        - identical = 1
        - different = 2
    - Column H: attendedItemsMatch
        - identical = 1
        - different = 0
        
Given the above, group data by condition -> a total of 4 possible conditions
''' 
# A=0 and K=0
data_cond_1 = conflict_data[(conflict_data['facesAreFearful']==0) & (conflict_data['facesAreAttended']==0)]
# A=0 and K=1
data_cond_2 = conflict_data[(conflict_data['facesAreFearful']==0) & (conflict_data['facesAreAttended']==1)]
# A=1 and K=0
data_cond_3 = conflict_data[(conflict_data['facesAreFearful']==1) & (conflict_data['facesAreAttended']==0)]
# A=1 and K=1
data_cond_4 = conflict_data[(conflict_data['facesAreFearful']==1) & (conflict_data['facesAreAttended']==1)]

data_conds = [data_cond_1, data_cond_2, data_cond_3, data_cond_4]
data_conds_avg_res_time = []
data_conds_cnt_right_ans = []
data_conds_cnt_wrong_ans = []

for data_cond in data_conds:
    # Get average response time for each condition
    # to handle different dtype
    if data_cond['SameDiffResponse.rt'].dtype in (['float','int']):
        data_conds_avg_res_time.append(data_cond['SameDiffResponse.rt'].mean())
    else:
        data_conds_avg_res_time.append(data_cond['SameDiffResponse.rt'].str.extract('(^[0-9]*.[0-9]*)', expand=False).dropna().astype(float).mean())

    # Count the number of right answers
    _cnt_right_ans = 0
    # to handle different dtype
    if data_cond['SameDiffResponse.rt'].dtype in (['float','int']):
        # H = S = identical
        _cnt_right_ans += len(data_cond[(data_cond['SameDiffResponse.keys']==1) & (data_cond['attendedItemsMatch']==1)])
        # H = S = different
        _cnt_right_ans += len(data_cond[(data_cond['SameDiffResponse.keys']==2) & (data_cond['attendedItemsMatch']==0)])
    else:
        # H = S = identical
        _cnt_right_ans += len(data_cond[(data_cond['SameDiffResponse.keys'].str.extract('(^[1-2])', expand=False).dropna().astype(int)==1) & (data_cond['attendedItemsMatch']==1)])
        # H = S = different
        _cnt_right_ans += len(data_cond[(data_cond['SameDiffResponse.keys'].str.extract('(^[1-2])', expand=False).dropna().astype(int)==2) & (data_cond['attendedItemsMatch']==0)])

    data_conds_cnt_right_ans.append(_cnt_right_ans)
    # Count # of wrong answers
    _cnt_wrong_ans = len(data_cond) - _cnt_right_ans
    data_conds_cnt_wrong_ans.append(_cnt_wrong_ans)

data_columns = ['Condition','Avg Response Time', 'Num of Right Ans', 'Numb of Wrong Ans']
data_label   = ['Fearful & Attended', 'Fearful & NOT Attended', 'NOT Fearful & Attended', 'NOT Fearful & NOT Attended']
data_out     = np.array([data_label,data_conds_avg_res_time,data_conds_cnt_right_ans,data_conds_cnt_wrong_ans]).transpose()
df_data_out  = pd.DataFrame(data=data_out, columns=data_columns)

save_filename = 'analyzed_' + os.path.splitext(os.path.basename(CSV_PATH))[0] + '.csv'
df_data_out.to_csv(save_filename, index=False)
print("[INFO] Output is saved as {}".format(save_filename))

