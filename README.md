
# Python Scripts for NCT-Lab 
This repository is for developing python scripts to generate a number of statistics from CSV files that contain experimental results for the following three different tasks:
* Task 1: N-back
* Task 2: Face-matching
* Task 3: BELT

## Requirements
In order to run the scripts, it is necessary to install the following library on your system:
* [Pandas](https://pandas.pydata.org/) (>=0.24.2)

## Usages
First, download the `Prod` folder to your local machine. Then run one of the following commands depending on your interest.

### :pushpin: *Task 1: N-back Analyzer*
To run the N-back analyzer,  open your terminal and execute the following command:
```console
user@local:~$ python <PATH/TO/analyze_Nback.py> -csv_main_path=<PATH/TO/XXX_Nback_XXX.csv> -csv_ref_path=<PATH/TO/nback_AB.csv>
```
For instance, if you downloaded the `Prod` folder to your local machine, say, under `~/Downloads`, and your main CSV (e.g., `AA06LC00_Nback_2021_Jun_09_1034.csv`) and `nback_AB.csv` is located at `~/Desktop/data`, the command should look like the following:
```console
user@local:~$ python ~/Downloads/Prod/Task1_N-Back/analyze_Nback.py -csv_main_path=~/Desktop/data/AA06LC00_Nback_2021_Jun_09_1034.csv -csv_ref_path=~/Desktop/data/nback_AB.csv
```
> **Note 1.** The path of csv_ref_path should be the same for running the other main CSV files.\
> **Note 2.** The script will generate two CSV files:

| Filename | Contents |
|---|---|
| *\<SUBJECTID\>*_avg_rxntime_per_loadsize.csv | Average response time per loadsize |
| *\<SUBJECTID\>*_avg_rxntime_per_stimulus.csv | Average response time per stimulus|

### :pushpin: *Task 2: Face-matching Analyzer*
Similar as above, open your terminal and execute the following command:
```console
user@local:~$ python <PATH/TO/analyze_FaceMatching.py> -csv_main_path=<PATH/TO/XXX_FaceMatching_XXX.csv> -csv_ref_path=<PATH/TO/facematching_AB.csv>
```
> **Note 1.** The path of csv_ref_path should be the same for running the other main CSV files.\
> **Note 2.** The script will generate two CSV files:

| Filename | Contents |
|---|---|
| *\<SUBJECTID\>*_avg_rxntime_per_condition.csv | Average response time per condition |
| *\<SUBJECTID\>*_avg_accuracy_per_condition.csv | Average accuracy per condition|

### :pushpin: *Task 3: BELT Analyzer*
Unlike the above two tasks, in order to run the script for the BELT task, a `.log` file corresponding to the main CSV file is required as following:
```console
user@local:~$ python <PATH/TO/analyze_BELT.py> -csv_path=<PATH/TO/XXX_BELT_XXX.csv> -log_path=<PATH/TO/XXX_BELT_XXX.log>
```
For instance, if you downloaded the `Prod` folder to your local machine, say, under `~/Downloads`, and your main CSV (e.g., `AA06LC00_BELT_TEST_2021_Jun_09_1320.csv`) and the corresponding log file (e.g., `AA06LC00_BELT_TEST_2021_Jun_09_1320.log` are located at `~/Desktop/data`, the command should look like the following:
```console
user@local:~$ python ~/Downloads/Prod/Task3_BELT/analyze_BELT.py -csv_path=~/Desktop/data/AA06LC00_BELT_TEST_2021_Jun_09_1320.csv -log_path=~/Desktop/data/AA06LC00_BELT_TEST_2021_Jun_09_1320.log
```
> **Note 1.** The path of log_path ***MUST be changed*** accordingly for running the each main CSV file.\
> **Note 2.** The script will generate the following CSV files:

| Filename | Contents |
|---|---|
| *\<SUBJECTID\>*_rxntime_from_onset_from_previous.csv | - Response time per presentation from onset stimulus <br> - Response time from previous stimulus|
| *\<SUBJECTID\>*_aggregated_stats.csv | Aggregated stats, including balloonscore per color, total balloonscores, average reaction time after popped, etc.|
| *\<SUBJECTID\>*_post_explosion_behavior.csv | Filtered results from _rxntime_from_onset_from_previous.csv to show every popped case and the right after of the same condition|


## Author
- Chulwoo (Mike) Pack 
 