## Requirements
In order to run the scripts, it is necessary to install the following library on your system:
* [Pandas](https://pandas.pydata.org/) (>=0.24.2)

## Usages
First, download the scripts to your local machine. Then run one of the following commands depending on your interest.

### :pushpin: *Task 1: BANDA Analyzer*
To run the BANDA analyzer,  open your terminal and execute the following command:
```console
user@local:~$ python <PATH/TO/analyze_banda.py> -csv_path=<PATH/TO/XXX_BANDA_XXX.csv>
```
For instance, if you downloaded the `analyze_banda.py` script to your local machine, say, under `~/Downloads`, and your  CSV (e.g., `BANDA014_Scanner_ABCD_conflict_2017_Jan_22_1515.csv`) is located at `~/Desktop/data`, the command should look like the following:
```console
user@local:~$ python ~/Downloads/analyze_banda.py -csv_path=~/Desktop/data/BANDA014_Scanner_ABCD_conflict_2017_Jan_22_1515.csv
```
> **Note .** The script will generate a single CSV file.

### :pushpin: *Task 2: Face-matching Analyzer*
To run the Face-matching analyzer,  open your terminal and execute the following command:
```console
user@local:~$ python <PATH/TO/analyze_facematching.py> -csv_path=<PATH/TO/XXX_FaceMatching_XXX.csv>
```
For instance, if you downloaded the `analyze_facematching.py` script to your local machine, say, under `~/Downloads`, and your  CSV (e.g., `BANDA014_Scanner_AB_FaceMatching_2017_Jan_22_1503.csv`) is located at `~/Desktop/data`, the command should look like the following:
```console
user@local:~$ python ~/Downloads/analyze_facematching.py -csv_path=~/Desktop/data/BANDA014_Scanner_AB_FaceMatching_2017_Jan_22_1503.csv
```
> **Note .** The script will generate a single CSV file.

## Author
- Chulwoo (Mike) Pack 