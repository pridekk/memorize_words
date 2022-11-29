import csv 
import json 

with open("words.csv", encoding="utf-8") as file:
    fields = ["word","meaning", "verb"]
    reader = csv.DictReader( file, fields)
    with open("words.json", "w", encoding="utf-8") as json_file:
        for row in reader:
            json.dump(row, json_file, ensure_ascii=False)
            json_file.write("\n")
