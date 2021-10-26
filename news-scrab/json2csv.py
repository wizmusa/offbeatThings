# -*- encoding: utf-8 -*-

import json

# 연도 별 파일 목록 읽기
f = open("docx_list_2018.txt", "r", encoding="UTF-8")
lines = f.readlines()

f2 = open("output_news_scrap_2018_entity.json", encoding="UTF-8")
json_data = f2.readlines()
result = ""

# extract text
for idx, json_string in enumerate(json_data):
    filename = lines[idx].strip("\n")
    print(filename)
    json_data = json.loads(json_string)
    
    for e in json_data["Entities"]:
        # print(e["Text"])
        result += filename + "," + e["Text"] + "," + e["Type"] + "," + str(e["Score"]) + "\n"
    
f.close()
f2.close()

f3 = open("result_2018.csv", "w", encoding="utf-8")
f3.write(result)
f3.close()

print('DONE')