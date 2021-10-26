import urllib.request
import sys
import re

argc = len(sys.argv)

if argc != 2:
	print('usage: python count.py url')
	exit()

path = sys.argv[1]

with urllib.request.urlopen(path) as response:
	html = response.read().decode("utf-8")

body = re.search('<body.*</body>', html, re.I|re.S)

if (body is None) :
	print ("No <body> in html")
	exit()

body = body.group()
body = re.sub('<script.*?>.*?</script>', '', body, 0, re.I|re.S)

text = re.sub('<.+?>', '', body, 0, re.I|re.S)


lines = text.splitlines()
text2 = ""
for line in lines:
    if len(line) > 100:
        text2 += line + "\n"


print(text2)

# nospace = re.sub('&nbsp;| |\t|\r|\n', '', text)
# print (nospace)