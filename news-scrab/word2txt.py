# -*- encoding: utf-8 -*-

import docx2txt

# 연도 별 파일 목록 읽기
f = open("docx_list_2018.txt", "r", encoding="UTF-8")
lines = f.readlines()

# extract text
for line in lines:
    filename = line.strip("\n")
    print(filename)
    text = docx2txt.process(filename)
	
    text2 = ""
    lines2 = text.splitlines()
    for line2 in lines2:
        if "조간 스크랩" in line2:
            continue
        elif " 경제지표" in line2:
            continue
        elif len(line2) < 16:
            continue
        else:
            text2 += line2
            text2 += "\n"
    
    text2 = text2.replace("–", "-") # replace utf-8 symbol (ndash) to ascii (-)
    text2 = text2.replace("•", "-") # replace utf-8 symbol (•) to ascii (-)

    f2 = open(filename + ".txt",'w')
    f2.write(text2)
    f2.close()

f.close()

print('DONE')