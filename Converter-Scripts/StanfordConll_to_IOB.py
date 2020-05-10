import codecs
import re


filename = "18181.txt"

#fileone = codecs.open("F:/Dropbox/Master/Plenarprotokolle/Annotiert/alle-final/Gold-18181-noAnhang.conll", "r", "utf-8")
fileone = codecs.open("F:/Dropbox/Master/"+filename+".conll", "r", "utf-8")
TextString = fileone.read()
#print(TextString)
TextList = TextString.splitlines()
#print(TextList)

newfile = open(r"F:/Dropbox/Master/"+filename+"_IOB.conll","w+", encoding="utf-8")


indi = 0
for x in TextList:
	if re.findall("PERSON", x) != []:
		#print("X:"+"		"+x+"\n"+"TextListindi:"+"	"+TextList[indi+1])
		TextList[indi] = re.sub("PERSON", "B-PER", TextList[indi])
		if re.findall("[B|I]-PER", TextList[indi-1]) != []:
			TextList[indi] = re.sub("B-PER", "I-PER", TextList[indi])
	elif re.findall("LOCATION", x) != []:
		#print("X:"+"		"+x+"\n"+"TextListindi:"+"	"+TextList[indi+1])
		TextList[indi] = re.sub("LOCATION", "B-LOC", TextList[indi])
		if re.findall("[B|I]-LOC", TextList[indi-1]) != []:
			TextList[indi] = re.sub("B-LOC", "I-LOC", TextList[indi])
	elif re.findall("ORGANIZATION", x) != []:
		#print("X:"+"		"+x+"\n"+"TextListindi:"+"	"+TextList[indi+1])
		TextList[indi] = re.sub("ORGANIZATION", "B-ORG", TextList[indi])
		if re.findall("[B|I]-ORG", TextList[indi-1]) != []:
			TextList[indi] = re.sub("B-ORG", "I-ORG", TextList[indi])
	elif re.findall("MISC", x) != []:
		#print("X:"+"		"+x+"\n"+"TextListindi:"+"	"+TextList[indi+1])
		TextList[indi] = re.sub("MISC", "B-MISC", TextList[indi])
		if re.findall("[B|I]-MISC", TextList[indi-1]) != []:
			TextList[indi] = re.sub("B-MISC", "I-MISC", TextList[indi])
	
	indi += 1

for x in TextList:
	newfile.write(x+"\n")

newfile.close()

#print(TextList)
	#if re.findall("PERSON|ORGANIZATION|LOCATION|OTHER", x):
		#print(x)