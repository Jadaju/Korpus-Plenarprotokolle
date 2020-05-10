import re
import codecs

fileone = codecs.open("F:/Dropbox/Master/Plenarprotokolle/Annotiert/GermaNER/09036-f-noAnhang-noConll.conll", "r", "utf-8")
TextString = fileone.read()
#print(TextString)
TextList = TextString.splitlines()
#print(TextList[28])

# if TextList[28] == "":
	# print("XS")

# a = re.split("  ", TextList[28])
# print(a[0])

newfile = open(r"F:\Dropbox\Master\GermaNERzuConll.conll","w+", encoding="utf-8")

#print(re.split("  " ,TextList[0]))
counter = 1
for x in TextList:
	a = re.split("  " , x)
	if x != "":
		#print("ja")
		#print(a)
		newfile.write(str(counter)+"	"+a[0]+"	"+"_"+"	"+"_"+"	"+a[1]+"	"+"_"+"	"+"_"+"\n")
		counter += 1
	else:
		#print("nein")
		newfile.write("\n")
		counter = 1

newfile.close()