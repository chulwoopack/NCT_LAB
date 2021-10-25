import os
import pandas as pd
import numpy as np
import argparse

'''
Parse Arguments
'''
parser = argparse.ArgumentParser(description='Analyze Face-matching')
parser.add_argument('-csv_main_path', type=str, required=True,
                   help='a path to the main CSV file (e.g., PARTICIPANTID_FaceMatching_YYYY_MMM_DD_XXXX.csv')
parser.add_argument('-csv_ref_path', type=str, required=True,
                   help='a path to the reference CSV file (e.g., facematching_AB.csv')
args = parser.parse_args()

CSV_MAIN_PATH = args.csv_main_path #'./data/AA06LC00_FaceMatching_2021_Jun_09_1112.csv'
CSV_REF_PATH  = args.csv_ref_path  #'./data/facematching_AB.csv'

print("[INFO] Processing {}...".format(CSV_MAIN_PATH))
      
subject_id = os.path.basename(CSV_MAIN_PATH).split('_')[0]
data_main = pd.read_csv(CSV_MAIN_PATH)
data_ref  = pd.read_csv(CSV_REF_PATH)

# Sanity check
assert len(data_main) == len(data_ref), "Assertion Failure: Please make sure if the number of data in {} matches that of in {}".format(CSV_REF_PATH, CSV_MAIN_PATH)

# Rename unnamed column of main.csv.
data_main.rename(columns={ data_main.columns[0]: "main_trial_id" }, inplace = True)

# Create a new data column 'main_trial_id' based on the'trial' column.
# The 'main_trial_id' column will be used to map (joining two tables) data between main.csv and ref.csv
data_ref['main_trial_id'] = (data_ref['trial']-1).values.astype(np.int)

# Join main.csv and ref.csv
data_merge = pd.merge(data_main, data_ref, on="main_trial_id")

# Goal 1: average response time per condition (neg, neu, pos, fruit, veg)
save_path = subject_id+"_avg_rxntime_per_condition.csv"
pd.DataFrame(data_merge.groupby('condition').mean().rxn_time).to_csv(save_path)
print("[INFO] Output is saved at {}".format(save_path))
# Goal 2: average accuracy per condition
save_path = subject_id+"_avg_accuracy_per_condition.csv"
pd.DataFrame(data_merge.groupby('condition').mean().percent_accuracy).to_csv(save_path)
print("[INFO] Output is saved at {}".format(save_path))

print("[INFO] Completed.")