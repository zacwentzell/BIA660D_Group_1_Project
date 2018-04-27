"""
Convert the JSONs in yelp_dataset/dataset to CSV
BIA660D - Group 1: Alec Kulakowski
"""
# Environment navigation
import os
project_path = [path for path in os.environ['PYTHONPATH'].split(";") if "group" in path.lower()][0]
dataset_path = project_path+"\\yelp_dataset\\dataset"
# JSON selection
json_list = [file for file in os.listdir(dataset_path) if ".json" in file]
for file_name in json_list:
