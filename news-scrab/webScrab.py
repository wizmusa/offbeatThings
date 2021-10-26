# -*- coding: utf-8 -*-

import urllib.request
import sys
import re


# 연도 별 파일 목록 읽기
f = open("docx_list_2018.txt", "r", encoding="UTF-8")
lines = f.readlines()

for line in lines:
    # 조간 스크랩 파일 목록 대로 뉴스기사 목록 파일을 읽는다.
    filename = line.strip("\n") + ".txt_url.txt"
    print(filename)
    
    f2 = open(filename, "r")
    lines2 = f2.readlines()
    text2 = ""
    
    # 뉴스 기사 목록 대로 웹 페이지를 읽어 plain text만 저장한다.
    for path in lines2:
        print(path)
        try:
            with urllib.request.urlopen(path) as response:
                html = response.read().decode("utf-8")
        except:
            print("It's not encoded with UTF-8.")
        
        if html == "":
            try:
                with urllib.request.urlopen(path) as response:
                    html = response.read().decode("euc-kr")
            except:
                print("It's not encoded with EUC-KR.")

        if html == "":
            try:
                with urllib.request.urlopen(path) as response:
                    html = response.read().decode("cp949")
            except:
                print("It's not encoded with CP949.")
                
        if html == "":
            try:
                with urllib.request.urlopen(path) as response:
                    html = response.read().decode("ISO-8859-1")
            except:
                print("It's not encoded with ISO-8859-1.")
        
        if html == "":
            print("Maybe forbidden.")
        
        text2 += "\n\n" + path
        
        body = re.search('<body.*</body>', html, re.I|re.S)
        html = "" # 초기화

        if (body is None) :
            print ("No <body> in html")
            continue

        body = body.group()
        body = re.sub('<script.*?>.*?</script>', '', body, 0, re.I|re.S)

        text = re.sub('<.+?>', '', body, 0, re.I|re.S)

        lines = text.splitlines()
        for line in lines:
            # 100글자가 넘는 줄만 뉴스 본문이라고 가정하여 저장한다. 
            if len(line.strip()) > 100:
                text2 += line.strip() + "\n"

                # text2 = text2.replace("–", "-") # replace utf-8 symbol (ndash) to ascii (-)
                # text2 = text2.replace("•", "-") # replace utf-8 symbol (•) to ascii (-)
                # text2 = text2.replace(u"\uF02c", "-") # replace utf-8 symbol \uf02c to ascii (-)
                # text2 = text2.replace(u"\uF020", "-") # replace utf-8 symbol \uf020 to ascii (-)
                # text2 = text2.replace(u"\uF030", "-") # replace utf-8 symbol \uf030 to ascii (-)
                # text2 = text2.replace(u"\uF032", "-") # replace utf-8 symbol \uf032 to ascii (-)
                # text2 = text2.replace(u"\u200b", "-") # replace utf-8 symbol \u200b to ascii (-)

    f2 = open(filename + "_news.txt", "wt", encoding="utf-8")
    f2.write(text2)
    f2.close()
f.close()