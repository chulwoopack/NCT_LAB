import os
import pandas as pd
import numpy as np
import argparse

# Ver. 3 (10/25/2021)

'''
Parse Arguments
'''
parser = argparse.ArgumentParser(description='Analyze N-back')
parser.add_argument('-csv_main_path', type=str, required=True,
                   help='a path to the main CSV file (e.g., PARTICIPANTID_Nback_YYYY_MMM_DD_XXXX.csv')
parser.add_argument('-csv_ref_path', type=str, required=True,
                   help='a path to the reference CSV file (e.g., nback_AB.csv')
args = parser.parse_args()

CSV_MAIN_PATH = args.csv_main_path #'./data/AA06LC00_Nback_2021_Jun_09_1034.csv'
CSV_REF_PATH  = args.csv_ref_path  #'./data/nback_AB.csv'
print("[INFO] Processing {}...".format(CSV_MAIN_PATH))

subject_id = os.path.basename(CSV_MAIN_PATH).split('_')[0]

# Read csv files and store them as dataframe
data_main = pd.read_csv(CSV_MAIN_PATH)
data_ref  = pd.read_csv(CSV_REF_PATH)

# Sanity check
#assert 2*len(data_main) == len(data_ref)

# Remove items having 'fix' trial_type in ref.csv
data_ref = data_ref[data_ref['trial_type'].astype(str) != 'fix']
# Create a new data column 'main_trial_id' based on the'trial' column.
# The 'main_trial_id' column will be used to map (joining two tables) data between main.csv and ref.csv
data_ref['main_trial_id'] = np.floor(data_ref['trial']/2).values.astype(np.int)

# Rename unnamed column of main.csv.
data_main.rename(columns={ data_main.columns[0]: "main_trial_id" }, inplace = True)

# Join main.csv and ref.csv
data_merge = pd.merge(data_main, data_ref, on="main_trial_id")
# Drop items showing instr.jpg
data_merge = data_merge[~data_merge['image_name'].str.endswith("back_instr.jpg")]

# Drop items incorrect answers
data_merge = data_merge[data_merge['corr_resp_x']==1]

# Drop items where rxn_time is NaN (meaning that the participant did not press the button, thus no rxn_time was recorded)
data_merge = data_merge.dropna(subset=['rxn_time'])

# Goal 1:  average response time per load size (0, 1, 2)
save_path = subject_id+"_avg_rxntime_per_loadsize.csv"
pd.DataFrame(data_merge.groupby('trial_type').mean().rxn_time).to_csv(save_path)
print("[INFO] Output is saved at {}".format(save_path))
# Goal 2: average response time per stimulus
save_path = subject_id+"_avg_rxntime_per_stimulus.csv"
pd.DataFrame.from_dict({"Avg_rxntime_per_stimulus":[data_merge.mean().rxn_time]}).to_csv(save_path, index=False)
print("[INFO] Output is saved at {}".format(save_path))
print("[INFO] Completed.")