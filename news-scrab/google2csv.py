# -*- encoding: utf-8 -*-

from googlesearch import search

# 연도 별 파일 목록 읽기
f = open("docx_list_2018a.txt", "r", encoding="UTF-8")
lines = f.readlines()

# query = "IPO시장 새해에도 활기 이어갈까뉴시스"
# for idx, result in enumerate(search(query, tld='com', lang='ko', num=1, start=0, stop=None, pause=0)):
    # if idx > 0:
	    # break
    
    # print(result)

# extract text
for line in lines:
    filename = line.strip("\n") + ".txt"
    print(filename)
    
    f2 = open(filename, "r")
    lines2 = f2.readlines()
    text2 = ""
    
    for line2 in lines2:
        for idx, result in enumerate(search(line2, tld='com', lang='ko', num=1, start=0, stop=None, pause=2)):
            if idx > 0:
                break
            print(result)
            text2 += result + "\n"

    f2 = open(filename + "_url.txt",'w')
    f2.write(text2)
    f2.close()

f.close()

print('DONE')