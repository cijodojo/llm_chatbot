import csv
import json

def csv_to_json(csv_file, json_file):
  data = []
  
  with open(csv_file, 'r', encoding='utf-8') as cf:
    csv_reader = csv.DictReader(cf)
    
    for row in csv_reader:
      data.append(row)
    
  with open(json_file, 'w', encoding='utf-8') as jf:
    json.dump(data, jf, indent=4)
    
csv_file_path = '../../dataset/insurance-dataset.csv'
json_file_path = '../../dataset/insurance-dataset.json'

csv_to_json(csv_file_path, json_file_path)