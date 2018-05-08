"""
Convert the JSONs in yelp_dataset/dataset to CSV
BIA660D - Group 1: Alec Kulakowski
"""
# Environment navigation
import os # import sys # import pandas as pd
import json
from pandas.io.json import json_normalize
project_path = [path for path in os.environ['PYTHONPATH'].split(";") if "group" in path.lower()][0]
dataset_path = project_path+"\\yelp_dataset\\dataset"
# Set WD: #   os.getcwd()     os.listdir()
os.chdir(dataset_path) #+"\\yelp_dataset\\json_to_csv"
file_list = [file for file in os.listdir() if ".json" in file] #os.listdir(dataset_path)
# Iterate through JSONs
file_list.remove("photos.json") # No need
file_list.remove("tip.json") # Irrelevant
for file_name in file_list:
    print("Converting "+file_name+" to Dataframe...")
    file_in = open(file_name, 'r')
    json_list = [json.loads(line) for line in file_in.read().split("\n") if "{" in line] # Sometimes empty lines
    df_temp = json_normalize(json_list)
    # os.remove(file_name.replace(".json", ".csv")) # No need
    df_temp.to_csv(file_name.replace(".json", ".csv"), index=False) # Use at end
    file_in.close()
    print("File saved: "+file_name.replace(".json",".csv"))

print("Done!")

# line_list = [line for line in file_in.read().split("\n") if "{" in line] # Sometimes empty lines
# json_list = list(map(json.loads, line_list))
# len(file_in.read().split("\n"))
# file_in.read()
# temp = pd.read_csv(file_name.replace(".json", ".csv"))
# temp = pd.read_json(file_name, lines=True) # There are some issues with nested JSON

### Old code from when we though json_to_csv would work, a number of the functions are depreciated and
### even when rectified, it breaks for certain files and returns completely blank CSVs for others.
# # # if not (project_path+"\\yelp_dataset\\json_to_csv" in sys.path):
# # #     sys.path.append(project_path+"\\yelp_dataset\\json_to_csv")
# # if not (project_path+"\\yelp_dataset" in sys.path):
# #     sys.path.append(project_path+"\\yelp_dataset")
# # import json_to_csv
# # # import json_to_csv_converter #execfile()
# # json_to_csv.json_to_csv_converter(json_list[0])
# os.system("python json_to_csv\json_to_csv_converter.py dataset\\business.json") # the resulting file is empty...
# # JSON selection
# json_list = [file for file in os.listdir(dataset_path) if ".json" in file]
# for file_name in json_list:
#     pass