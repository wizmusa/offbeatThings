# -*- encoding: utf-8 -*-
import json

f2 = open("title_2018.json", encoding="UTF-8")
json_data = f2.readlines()
result = ""

# extract text
for idx, json_string in enumerate(json_data):
    json_data = json.loads(json_string)
    
    for e in json_data["Entities"]:
        # print(e["Text"])
        eText = e["Text"].strip()
        if eText.find("\n"):            
            eText = eText[eText.find("\n")+1:].strip()
        
        result += eText + "," + e["Type"] + "," + str(e["Score"]) + "\n"        
    
f2.close()

f3 = open("title_result_2018.csv", "w", encoding="utf-8")
f3.write(result)
f3.close()

print('DONE')