import codecs
import re

#wähle aus "01143", "09036", "18181" oder selbst annotierte.
Protokoll = "18181"
#wähle aus "Stanford", "GermaNER", "spacy", "Gold"; Tagger2 sollte Goldstandard sein für Vergleich
Tagger1 = "Stanford"
Tagger2 = "Gold"

### lies Dateien ein
fileone = codecs.open("F:/Dropbox/Master/Plenarprotokolle/Annotiert/Evaluation/"+Tagger1+"-"+Protokoll+"-gazetteer-common-crawl_IOB.conll", "r", "utf-8")
filetwo = codecs.open("F:/Dropbox/Master/Plenarprotokolle/Annotiert/Evaluation/"+Tagger2+"-"+Protokoll+".conll", "r", "utf-8")

### Dateien zu Strings
TextString1 = fileone.read()
TextString2 = filetwo.read()

### entferne leere Zeilen (Markierung für neue Sätze)
TextString1 = re.sub(r"\n\r\n", "\n", TextString1)
TextString2 = re.sub(r"\n\r\n", "\n", TextString2)
### entferne "leere" Zeilen bei spacy
TextString1 = re.sub("[0-9]+\t\t.+\r\n", "", TextString1)
TextString2 = re.sub("[0-9]+\t\t.+\r\n", "", TextString2)
TextString1 = re.sub("[0-9]+\t +\t.+\r\n", "", TextString1)
TextString2 = re.sub("[0-9]+\t +\t.+\r\n", "", TextString2)
TextString1 = re.sub(" ", " ", TextString1)
TextString2 = re.sub(" ", " ", TextString2)

### ersetzte "OTH" durch "MISC" bei GermaNER
TextString1 = re.sub("OTH", "MISC", TextString1)
TextString2 = re.sub("OTH", "MISC", TextString2)

### Ändere Gedankenstriche/Hyphen etc.
#TextString3 = re.sub("–", "--", TextString3)
#TextString3 = re.sub("“", "``", TextString3)
TextString1 = re.sub("–", "--", TextString1)
TextString1 = re.sub("“", "``", TextString1)
TextString2 = re.sub("–", "--", TextString2)
TextString2 = re.sub("“", "``", TextString2)

### Lies Token in Liste ein
TextList1 = TextString1.splitlines()
TextList2 = TextString2.splitlines()
#TextList3 = TextString3.splitlines()
#TextListGold = TextStringGold.splitlines()

###Kopie zu Testzwecken
GoldKopie = TextList2.copy()

### Ordnet Tagger Namen entsprechende Liste zu für main(Tagger1, Tagger2)
# Tagger = {
	# "Stanford": TextList1,
	# "GermaNER": TextList2,
	# "spacy": TextList3,
	# "Gold": TextListGold
	# }


### globale Variablen
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
searchList = ["B-PER", "I-PER", "B-LOC", "I-LOC", "B-ORG", "I-ORG", "B-MISC", "I-MISC"]
shortIsearchList = ["I-PER", "I-LOC", "I-ORG", "I-MISC"]
shortBsearchList = ["B-PER", "B-LOC", "B-ORG", "B-MISC"]
shortSearchList = ["PER", "LOC", "ORG", "MISC"]
resultArray = [[],[],[]]
### COR, INC, PAR, MIS, SPU, Precision, Recall, F1 für jedes Measure
resultMeasures =[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
average = []
List_SPU = []
List_MIS = []
TagCount = []

### Hash für Tags in Goldstandard (Tagger2)
GoldTags = {
		"B-PER": 0,
		"I-PER": 0,
		"B-LOC": 0,
		"I-LOC": 0,
		"B-ORG": 0,
		"I-ORG": 0,
		"B-MISC": 0,
		"I-MISC": 0,
		"Gesamt": 0
		}

### Zählt alle Tags in der übergebenen Datei
def countGold(file):
	global GoldTags, searchList
	
	for x in file:
		for y in searchList:
			if re.findall("\t"+y+"\t_\t_", x) != []:
				GoldTags[y] += 1
				GoldTags["Gesamt"] += 1


def print_word_count(file):

	countDic = {
		"B-PER": [],
		"I-PER": [],
		"B-LOC": [],
		"I-LOC": [],
		"B-ORG": [],
		"I-ORG": [],
		"B-MISC": [],
		"I-MISC": [],
}
	count_list = []	
	for x in file:
		for y in searchList:
			if re.findall("\t"+y+"\t_\t_", x) != []:
				asdf = x.split()
				countDic[asdf[4]].append(asdf[1])
	
	for x in countDic:
		counts = dict()
		for word in countDic[x]:
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1
		count_list.append(counts)
	
	it = 0
	for x in count_list:
		#print(sorted(x.items(), key=lambda item: item[1]))
		count_list[it] = sorted(x.items(), key=lambda item: item[1], reverse=True)
		it += 1
	
	print("Word_Count:")
	for x in count_list:
		print(x)
	return count_list


def print_Metric(metric):
	countDic = {
	"O": []
}	
	count_list = []

	#print(metric)
	
	for x in metric:
		asdf = x.split()
		countDic["O"].append(asdf[1])
	
	for x in countDic:
		counts = dict()
		for word in countDic[x]:
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1
		count_list.append(counts)
	
	it = 0
	for x in count_list:
		#print(sorted(x.items(), key=lambda item: item[1]))
		count_list[it] = sorted(x.items(), key=lambda item: item[1], reverse=True)
		it += 1
	
	print("Count:")
	for x in count_list:
		print(x)
		print()
	return count_list

allTags = {
	"B-PER_TP": 0,
	"B-PER_FN": 0,
	"B-PER_FP": 0,
	"I-PER_TP": 0,
	"I-PER_FN": 0,
	"I-PER_FP": 0,
	"B-LOC_TP": 0,
	"B-LOC_FN": 0,
	"B-LOC_FP": 0,
	"I-LOC_TP": 0,
	"I-LOC_FN": 0,
	"I-LOC_FP": 0,
	"B-ORG_TP": 0,
	"B-ORG_FN": 0,
	"B-ORG_FP": 0,
	"I-ORG_TP": 0,
	"I-ORG_FN": 0,
	"I-ORG_FP": 0,
	"B-MISC_TP": 0,
	"B-MISC_FN": 0,
	"B-MISC_FP": 0,
	"I-MISC_TP": 0,
	"I-MISC_FN": 0,
	"I-MISC_FP": 0
	}

strictEval = {
	"COR": 0,
	"INC": 0,
	"PAR": 0,
	"MIS": 0,
	"SPU": 0
	}
exactEval = {
	"COR": 0,
	"INC": 0,
	"PAR": 0,
	"MIS": 0,
	"SPU": 0
	}
partialEval = {
	"COR": 0,
	"INC": 0,
	"PAR": 0,
	"MIS": 0,
	"SPU": 0
	}
typeEval = {
	"COR": 0,
	"INC": 0,
	"PAR": 0,
	"MIS": 0,
	"SPU": 0
	}

### Performance per label type per token
def checkNERperLabel(it1, it2):
	global searchList
	String1 = TextList1[it1]
	String2 = TextList2[it2]

	for x in searchList:
		if re.findall("\tO\t_\t_", String1) == [] or re.findall("\tO\t_\t_", String2) == []:
			if re.findall("\t"+x+"\t_\t_", String1) != [] and re.findall("\t"+x+"\t_\t_", String2) != []:
				allTags[x+"_TP"] += 1
				#print(x+"_TP:	"+String1+"		"+String2+"\n")
			elif re.findall("\t"+x+"\t_\t_", String1) == [] and re.findall("\t"+x+"\t_\t_", String2) != []:
				allTags[x+"_FN"] += 1
				#if x == "B-PER" or x == "B-PER":
					#print(x+"_FN:	"+String1+"		"+String2+"\n")
				#print(x+"_FN:	"+String1+"		"+String2+"\n")
			elif re.findall("\t"+x+"\t_\t_", String1) != [] and re.findall("\t"+x+"\t_\t_", String2) == []:
				allTags[x+"_FP"] += 1
				#if x == "B-ORG" or x == "I-ORG":
					#print(x+"_FP:	"+String1+"		"+String2+"\n")
				#print(x+"_FP:	"+String1+"		"+String2+"\n")
				
### Vergleicht 2 Token wenn einer oder beide nicht O ist/sind
def checkNER(it1, it2):
	global strictEval, exactEval, partialEval, typeEval
	String1 = TextList1[it1]
	String2 = TextList2[it2]
	
	strict = False
	exact = False
	partial = False
	type = False
	
	#print("Strings:	"+String1+"	"+String2)
	
	missing = checkMissing(it1, it2)
	spurious = checkSpurious(it1, it2)
	
	### nicht MIS und nich SPU und nur für System = B-type (verhindert doppelte Zählung von INC und PAR)
	if not missing and not spurious and re.findall("\tB-.+\t_\t_", String1) != []:
		strict = checkStrict(it1, it2)
		exact = checkExact(it1, it2)
		partial = checkPartial(it1, it2)
		type = checkType(it1, it2)
	else:
		#print("MIS or SPU:	"+String1+"	"+String2)
		pass
	
	if missing or strict or exact or partial or type:
		GoldKopie[it2] = re.sub("B-","GEFUNDEN-", GoldKopie[it2])
		pass
	elif spurious:
		#print("SPURIOUS:	"+String1+"	"+String2+"\n")
		pass
	### 1 = I-type und 2 = B-type. Wurde durch B-type bei 1 in vorherigen Fällen schon berücksichtigt.
	elif re.findall("\tI-.+\t_\t_", String1) != [] and re.findall("\tB-.+\t_\t_", String2) != []:
		#print("Done:	"+String1+"	"+String2+"\n")
		pass
	else:
		#print("Analyse:	"+String1+"	"+String2)
		#print("Analyse:	"+TextList1[it1+1]+"	"+TextList2[it2+1]+"\n")
		pass




def checkStrict(it1, it2):
	String1 = TextList1[it1]
	String2 = TextList2[it2]	
	
	if checkBoundary(it1, it2):
		for x in shortBsearchList:
			### wenn gleicher B-type
			if re.findall(x, String1) != [] and re.findall(x, String2) != []:
				strictEval["COR"] += 1
				#print("Strict CORRECT:	"+x+"	"+String1+"	"+String2)
				return True
			### B-types stimmen nicht überein
			elif x == "B-MISC":
				#print("Strict INCORRECT:	"+x+"	"+String1+"	"+String2)
				strictEval["INC"] += 1
				return False
	### nicht gleiche Grenzen
	else:
		strictEval["INC"] += 1
		#print("Strict INCORRECT:	"+String1+"	"+String2)
		return False

def checkExact(it1, it2):
	String1 = TextList1[it1]
	String2 = TextList2[it2]
	
	if checkBoundary(it1, it2):
		exactEval["COR"] += 1
		return True
	elif re.findall("\tB-.+\t_\t_", String1) != [] or re.findall("\tB-.+\t_\t_", String2) != []:
		exactEval["INC"] += 1
		return False
	else:
		return False

def checkPartial(it1, it2):
	String1 = TextList1[it1]
	String2 = TextList2[it2]
	
	### wenn exact, dann auch partial
	if checkBoundary(it1, it2):
		partialEval["COR"] += 1
		return True
	elif re.findall("\tB-.+\t_\t_", String1) != [] or re.findall("\tB-.+\t_\t_", String2) != []:
		partialEval["PAR"] += 1
		return True
	### sollte nie eintreten
	else:
		partialEval["INC"] += 1
		return False

def checkType(it1, it2):
	String1 = TextList1[it1]
	String2 = TextList2[it2]
	
	#print("CHECK TYPE:	"+String1+"	"+String2)
	
	### wenn exact
	if checkBoundary(it1, it2):
		for x in shortBsearchList:
			### wenn type übereinstimmt True
			if re.findall(x, String1) != [] and re.findall(x, String2) != []:
				#print("TYPE CORRECT1:	"+x+"	"+String1+"	"+String2)
				typeEval["COR"] += 1
				return True
			### ansonsten False wenn letztes x erreicht wurde
			elif x == "B-MISC":
				#print("TYPE INCORRECT1:	"+x+"	"+String1+"	"+String2)
				typeEval["INC"] += 1
	### wenn nicht exact
	elif re.findall("\tB-.+\t_\t_", String1) != [] or re.findall("\tB-.+\t_\t_", String2) != []:
		#print("CHECK TYPE OOB:	"+String1+"	"+String2)
		for x in shortSearchList:
			### Abbruchbedingung für Listenende
			if it1+1 > len(TextList1)-1 or it2+1 > len(TextList2)-1:
				for y in shortSearchList:
					if re.findall(y, String1) != [] and re.findall(y, String2) != []:
						#print("TYPE CORRECT2:	"+x+"	"+String1+"	"+String2)
						typeEval["COR"] += 1
						return True
					elif y == "MISC":
						#print("TYPE INCORRECT2:	"+x+"	"+String1+"	"+String2)
						typeEval["INC"] += 1
						return False
					else:
						pass
			if re.findall(x, String1) != [] and re.findall(x, TextList2[it2+1]) != [] or re.findall(x, TextList1[it1+1]) != [] and re.findall(x, String2) != [] or re.findall(x, String1) != [] and re.findall(x, String2) != []: 
				#print("TYPE CORRECT3:	"+x+"	"+String1+"	"+String2)
				#print("TYPE CORRECT3:	"+x+"	"+TextList1[it1+1]+"	"+TextList2[it2+1]+"\n")
				typeEval["COR"] += 1
				return True
			elif x == "MISC":
				#print("TYPE INCORRECT3:	"+x+"	"+String1+"	"+String2)
				typeEval["INC"] += 1
				#print("String1:		"+String1+"			"+"String2:		"+String2)
				#print("String1:		"+List1[it1+1]+"		"+"String2:	"+List2[it2+1]+"\n")
	elif re.findall("\tO\t_\t_", String1) == [] and re.findall("\tO\t_\t_", String2) == []:
		#print("CHECK TYPE SOLLTE NICHT PASSIEREN:	"+String1+"	"+String2)
		pass
	else:
		#print("CHECK TYPE SOLLTE NICHT PASSIEREN:	"+String1+"	"+String2)
		pass

def checkMissing(it1, it2):
	String1 = TextList1[it1]
	String2 = TextList2[it2]
	
	### wenn System O ist und Gold B-type
	if re.findall("\tO\t_\t_", String1) != [] and re.findall("\tB-.+\t_\t_", String2) != []:
		#print("MISSING Beginn:	"+String1+"	"+String2)
		for i in range(1, 20):
			### Abruchbedingung am Listenende
			if it1+i > len(TextList1)-1 or it2+i > len(TextList2)-1:
				#print("ENDE ERREICHT")
				strictEval["MIS"] += 1
				exactEval["MIS"] += 1
				partialEval["MIS"] += 1
				typeEval["MIS"] += 1
				List_MIS.append(String1+"	"+String2)
				return True
			#wenn Gold O ist oder Gold neuer B-type
			if re.findall("\tO\t_\t_", TextList2[it2+i]) != [] or re.findall("\tB-.+\t_\t_", TextList2[it2+i]) != []:
				#print("MISSING True:	"+TextList1[it1+i]+"	"+TextList2[it2+i]+"\n")
				strictEval["MIS"] += 1
				exactEval["MIS"] += 1
				partialEval["MIS"] += 1
				typeEval["MIS"] += 1
				List_MIS.append(String1+"	"+String2)
				return True
			elif re.findall("\tI-.+\t_\t_", TextList2[it2+i]) != [] and re.findall("\tO\t_\t_", TextList1[it1+i]) != []:
				#print("MISSING Continue:	"+TextList1[it1+i]+"	"+TextList2[it2+i])
				pass
			else:
				#print("MISSING False 1:	"+TextList1[it1+i]+"	"+TextList2[it2+i])
				return False
	else:
		#print("MISSING False 2:	"+String1+"	"+String2+"\n")
		return False

def checkSpurious(it1, it2):
	String1 = TextList1[it1]
	String2 = TextList2[it2]
	#print(String1)
	
	### System hat B-type, Gold ist O
	if re.findall("\tB-.+\t_\t_", String1) != [] and re.findall("\tO\t_\t_", String2) != []:
		#print("SPURIOUS Beginn:	"+String1+"	"+String2)
		for i in range(1, 20):
			### Abruchbedingung am Listenende
			if it1+i > len(TextList1)-1 or it2+i > len(TextList2)-1:
				#print("ENDE ERREICHT")
				strictEval["SPU"] += 1
				exactEval["SPU"] += 1
				partialEval["SPU"] += 1
				typeEval["SPU"] += 1
				List_SPU.append(String1+"	"+String2)
				return True
			### wenn das nächste von System O oder ein neues B-type ist
			if re.findall("\tB-.+\t_\t_", TextList1[it1+i]) != [] or re.findall("\tO\t_\t_", TextList1[it1+i]) != []:
				#print("SPURIOUS True:	"+String1+"	"+String2)
				#print("SPURIOUS True:	"+TextList1[it1+i]+"	"+TextList2[it2+i]+"\n")
				strictEval["SPU"] += 1
				exactEval["SPU"] += 1
				partialEval["SPU"] += 1
				typeEval["SPU"] += 1
				List_SPU.append(String1+"	"+String2)
				return True
			### wenn das nächste von System einer Inner type ist und das nächste von Gold O ist -> weitermachen mit i+1
			elif re.findall("\tI-.+\t_\t_", TextList1[it1+i]) != [] and re.findall("\tO\t_\t_", TextList2[it2+i]) != []:
				#print("SPURIOUS Continue:	"+TextList1[it1+i]+"	"+TextList2[it2+i])
				pass
			### sonst nicht SPU
			else:
				#print("SPURIOUS False:	"+String1+"	"+String2)
				#print("SPURIOUS False:	"+TextList1[it1+i]+"	"+TextList2[it2+i]+"\n")
				return False
	else:
		return False

def checkBoundary(it1, it2):
	String1 = TextList1[it1]
	String2 = TextList2[it2]
	
	### selber start mit B- types
	if re.findall("\tB-.+\t_\t_", String1) != [] and re.findall("\tB-.+\t_\t_", String2) != []:
		#print("Boundary Beginn:	"+String1+"	"+String2)
		for i in range(1,20):
			### Abruchbedingung am Listenende
			if it1+i > len(TextList1)-1 or it2+i > len(TextList2)-1:
				print("ENDE ERREICHT")
				return True
			if re.findall("\tO\t_\t_", TextList1[it1+i]) != [] and re.findall("\tO\t_\t_", TextList2[it2+i]) != [] or re.findall("\tB-.+\t_\t_", TextList1[it1+i]) != [] and re.findall("\tB-.+\t_\t_", TextList2[it2+i]) != []or re.findall("\tB-.+\t_\t_", TextList1[it1+i]) != [] and re.findall("\tO\t_\t_", TextList2[it2+i]) != [] or re.findall("\tO\t_\t_", TextList1[it1+i]) != [] and re.findall("\tB-.+\t_\t_", TextList2[it2+i]) != []:
				#print("Boundary True:	"+String1+"	"+String2)
				#print("Boundary:	"+List1[it1+i]+"	"+List2[it2+i]+"\n")
				return True
			elif re.findall("\tI-.+\t_\t_", TextList1[it1+i]) != [] and re.findall("\tI-.+\t_\t_", TextList2[it2+i]) != []:
				#print("Boundary Continue:	"+List1[it1+i]+"	"+List2[it2+i])
				continue
			else:
				#print("Boundary False:	"+List1[it1+i]+"	"+List2[it2+i]+"\n")
				return False
	else:
		#print("Boundary False:	"+String1+"	"+String2+"\n")
		return False



### HAUPTMETHODE zur Sequenzierung
def main(TextVergleich1, TextVergleich2):
	global count1, count2, count3, count4, count5
	it = 0
	iterator = 0
	last1 = ""
	last2 = ""
	buildlast1 = ""
	for x in TextVergleich1:
		match1 = re.sub("[0-9]+\t", "", x, 1)
		match1 = re.sub("\t_\t_.+", "" , match1)
		match1 = re.sub("\t.+", "" , match1)
		#print(match1)
		match2 = re.sub("[0-9]+\t", "", TextVergleich2[it], 1)
		match2 = re.sub("\t_\t.+", "" , match2)
	
		#print("MATCH2:	"+match2)
	
		if match1 == match2 or match1 == "-LRB-" and match2 == "(" or match1 == "-RRB-" and match2 == ")" or match1 == "--" and match2 == "—" or match1 == "``" and match2 == "„" or match1 == "''" and match2 == "\"" or match1 == "-LSB-" and match2 == "[" or match1 == "-RSB-" and match2 == "]" or match1 == "`" and match2 == "'" or match2 == "-LRB-" and match1 == "(" or match2 == "-RRB-" and match1 == ")" or match2 == "--" and match1 == "—" or match2 == "``" and match1 == "„" or match2 == "''" and match1 == "\"" or match2 == "-LSB-" and match1 == "[" or match2 == "-RSB-" and match1 == "]" or match2 == "`" and match1 == "'" or match1 == ". . . ." and match2 == "..." or match1 == ". . ." and match2 == "...":
			#print("Fall1:"+"	"+match1+"		"+match2)
			count1 += 1
			### überprüfe NER wenn einer der beiden Token als Beginn eines NE getaggt ist
			if re.findall("\tB-.+\t_\t_", TextVergleich1[iterator]) != [] or re.findall("\tB-.+\t_\t_", TextVergleich2[it]) != []:
				checkNER(iterator, it)
			checkNERperLabel(iterator, it)
			it += 1
		elif match1 in match2:
			#print("Fall2:"+"	"+match1+"		"+match2)
			count2 += 1
			#print("last1:"+"	"+last1)
			#print("last2:"+"	"+last2)
			buildlast1 = buildlast1+match1
			if buildlast1 == match2:
				#print("Fall2 Match")
				it += 1
				buildlast1 = ""		
			### seltener Fall, bei dem ein Satzzeichen noch an das nächste token vorangestellt wird (spacy, Fehler)
			elif last2+match1 == match2:
				#print("RARE")
				it +=1
				buildlast1 = ""
			### seltener Fall, bei dem token nicht getrennt sind, Bsp.: '1 3/4' bleibt zusammen als 1 Token. Jedoch sind 1 und 3 nicht durch normales Leerzeichen getrennt
			elif last1+" "+match1 == match2:
				#print("RARE")
				it +=1
				buildlast1 = ""
		elif match2 in match1:
			#print("Fall3:"+"	"+match1+"		"+match2)
			count3 += 1
			for i in range(100):
				matchx = re.sub("[0-9]+\t", "", TextVergleich2[it+1], 1)
				matchx = re.sub("\t_\t.+", "" , matchx)
				#print("matchx:"+"	"+match1+"		"+matchx)
				if matchx in match1:
					match2 = matchx
					it += 1
				else:
					it += 1
					break
		elif match1 in last2:
			#skipt 1 mal x / Sonderfall durch Tokenisierungsfehler. it wird nicht hochgezählt
			#print("Fall4:"+"	"+match1+"		"+match2)
			count4 += 1
			if last1 == "." and last2 == "...":
				#print("Sonderfall")
				match2 = last2
		### Sonderfall Ampersand / &-Zeichen
		elif last1 == "&" and last2 == "&" or last1 == "amp" and last2 == "&":
			#print("Fall5:"+"	"+match1+"		"+match2)
			match2 = last2
			count5 += 1
			it += 0
		else:
			print("nomatch:"+"	"+match1+"		"+match2)
			print("last1:"+"	"+last1)
			print("last2:"+"	"+last2)
			print("buildlast1:"+"	"+buildlast1)
			print("ITERATOR1:	"+str(iterator)+"	ITERATOR2:	"+str(it))
			break
	
		buildlast2 = ""
		last1 = match1
		last2 = match2
		iterator += 1
		### Notstopp bei unterschiedlichem Ende
		if iterator > len(TextList1)-1 or it > len(TextList2)-1:
			#print("ENDE ERREICHT?"+last1+"	"+last2)
			break

def Fall_Counter():
	print("Fall1:"+"	"+str(count1))
	print("Fall2:"+"	"+str(count2))
	print("Fall3:"+"	"+str(count3))
	print("Fall4:"+"	"+str(count4))
	print("Fall5:"+"	"+str(count5))

##precision, recall, f1-score per label type per token
def calculateResults():
	global searchList, resultArray, average, TagCount
	for x in searchList:
		### precision
		if (allTags[x+"_TP"]+allTags[x+"_FP"]) == 0:
			precision = 1.0
		else:
			precision = round(allTags[x+"_TP"]/(allTags[x+"_TP"]+allTags[x+"_FP"]), 3)
		resultArray[0].append(precision)
		### recall
		if (allTags[x+"_TP"]+allTags[x+"_FN"]) == 0:
			recall = 1.0
		else:
			recall = round(allTags[x+"_TP"]/(allTags[x+"_TP"]+allTags[x+"_FN"]), 3)
		resultArray[1].append(recall)
		### f1-score
		if (precision+recall) == 0:
			f1 = 0.0
		else:
			f1 = round(2*(precision*recall)/(precision+recall), 3)
		resultArray[2].append(f1)
	
	Gesamtzahl = 0
	for x in allTags:
		Gesamtzahl = Gesamtzahl + allTags[x]
	#print("Gesamtzahl:	"+str(Gesamtzahl))
	for x in resultArray:
		sum = 0
		if x != []:
			sum = x[0] * (allTags["B-PER_TP"]+allTags["B-PER_FN"]+allTags["B-PER_FP"]) + x[1] * (allTags["I-PER_TP"]+allTags["I-PER_FN"]+allTags["I-PER_FP"]) + x[2] * (allTags["B-LOC_TP"]+allTags["B-LOC_FN"]+allTags["B-LOC_FP"]) + x[3] * (allTags["I-LOC_TP"]+allTags["I-LOC_FN"]+allTags["I-LOC_FP"]) + x[4] * (allTags["B-ORG_TP"]+allTags["B-ORG_FN"]+allTags["B-ORG_FP"]) + x[5] * (allTags["I-ORG_TP"]+allTags["I-ORG_FN"]+allTags["I-ORG_FP"]) + x[6] * (allTags["B-MISC_TP"]+allTags["B-MISC_FN"]+allTags["B-MISC_FP"]) + x[7] * (allTags["I-MISC_TP"]+allTags["I-MISC_FN"]+allTags["I-MISC_FP"])
		average.append(round(sum/Gesamtzahl, 3))
	
	for x in searchList:
		TagCount.append(allTags[x+"_TP"]+allTags[x+"_FN"]+allTags[x+"_FP"])
	gesamt = 0
	for x in TagCount:
		gesamt += x
	TagCount.append(gesamt)
	
	calcMeasures()
	
def calcMeasures():
	### berechne possible und actual (= TP + FN | TP + FP)
	possible = strictEval["COR"] + strictEval["INC"] + strictEval["PAR"] + strictEval["MIS"]
	actual = strictEval["COR"] + strictEval["INC"] + strictEval["PAR"] + strictEval["SPU"]
	
	### strict
	resultMeasures[0][0] = strictEval["COR"]
	resultMeasures[0][1] = strictEval["INC"]
	resultMeasures[0][2] = strictEval["PAR"]
	resultMeasures[0][3] = strictEval["MIS"]
	resultMeasures[0][4] = strictEval["SPU"]
	if actual > 0:
		precision = strictEval["COR"] / actual
	else:
		precision = 1
	resultMeasures[0][5] = precision
	recall = strictEval["COR"] / possible
	resultMeasures[0][6] = recall
	if precision+recall != 0:
		f1 = 2*(precision*recall)/(precision+recall)
	else:
		f1 = 0
	resultMeasures[0][7] = f1
	#exact
	resultMeasures[1][0] = exactEval["COR"]
	resultMeasures[1][1] = exactEval["INC"]
	resultMeasures[1][2] = exactEval["PAR"]
	resultMeasures[1][3] = exactEval["MIS"]
	resultMeasures[1][4] = exactEval["SPU"]
	if actual > 0:
		precision = exactEval["COR"] / actual
	else:
		precision = 1
	resultMeasures[1][5] = precision
	recall = exactEval["COR"] / possible
	resultMeasures[1][6] = recall
	if precision+recall != 0:
		f1 = 2*(precision*recall)/(precision+recall)
	else:
		f1 = 0
	resultMeasures[1][7] = f1
	### partial
	resultMeasures[2][0] = partialEval["COR"]
	resultMeasures[2][1] = partialEval["INC"]
	resultMeasures[2][2] = partialEval["PAR"]
	resultMeasures[2][3] = partialEval["MIS"]
	resultMeasures[2][4] = partialEval["SPU"]
	if actual > 0:
		precision = (partialEval["COR"] + 0.5 * partialEval["PAR"]) / actual
	else:
		precision = 1
	resultMeasures[2][5] = precision
	recall = (partialEval["COR"] + 0.5 * partialEval["PAR"]) / possible
	resultMeasures[2][6] = recall
	if precision+recall != 0:
		f1 = 2*(precision*recall)/(precision+recall)
	else:
		f1 = 0
	resultMeasures[2][7] = f1
	### type
	resultMeasures[3][0] = typeEval["COR"]
	resultMeasures[3][1] = typeEval["INC"]
	resultMeasures[3][2] = typeEval["PAR"]
	resultMeasures[3][3] = typeEval["MIS"]
	resultMeasures[3][4] = typeEval["SPU"]
	if actual > 0:
		precision = (typeEval["COR"] + 0.5 * typeEval["PAR"]) / actual
	else:
		precision = 1
	resultMeasures[3][5] = precision
	recall = (typeEval["COR"] + 0.5 * typeEval["PAR"]) / possible
	resultMeasures[3][6] = recall
	if precision+recall != 0:
		f1 = 2*(precision*recall)/(precision+recall)
	else:
		f1 = 0
	resultMeasures[3][7] = f1

def printResult():
	print()
	print("TagCount:")
	print(TagCount)
	print()
	print("AlleTags:")
	print(allTags)
	print("GoldTags:")
	print(GoldTags)
	print("ResultArray:")
	print(resultArray)
	print("Durchschnitt:")
	print(average)
	print()
	print("StrictEval:")
	print(strictEval)
	print("ExactEval:")
	print(exactEval)
	print("PartialEval:")
	print(partialEval)
	print("TypeEval:")
	print(typeEval)
	print("\n"+"ResultMeasures:")
	for x in resultMeasures:
		for y in x:
			print(round(y, 3), end=" ")
		print("\n")
	#print(resultMeasures)
	
	print("Gesamt-B-Gold:	"+str(GoldTags["B-PER"]+GoldTags["B-LOC"]+GoldTags["B-ORG"]+GoldTags["B-MISC"]))
	print("Gesamt-B-Eval:	"+str(strictEval["COR"]+strictEval["INC"]+strictEval["MIS"])+"\n")
	#print(GoldKopie)
	#print("List_SPU:")
	#for x in List_SPU:
		#print(x)
	#print("List_MIS:")
	#for x in List_MIS:
		#print(x)
		
def printforlatex():
	print("Token-Level:")
	print("B-PER & "+str(round(resultArray[0][0], 3))+" & "+str(round(resultArray[1][0], 3))+" & "+str(round(resultArray[2][0], 3))+" & "+str(TagCount[0])+" & "+str(allTags["B-PER_TP"])+" & "+str(allTags["B-PER_FP"])+" & "+str(allTags["B-PER_FN"])+" & "+str(GoldTags["B-PER"])+"\\\\\\cline{2-9}")
	print("I-PER & "+str(round(resultArray[0][1], 3))+" & "+str(round(resultArray[1][1], 3))+" & "+str(round(resultArray[2][1], 3))+" & "+str(TagCount[1])+" & "+str(allTags["I-PER_TP"])+" & "+str(allTags["I-PER_FP"])+" & "+str(allTags["I-PER_FN"])+" & "+str(GoldTags["I-PER"])+"\\\\\\cline{2-9}")
	print("B-LOC & "+str(round(resultArray[0][2], 3))+" & "+str(round(resultArray[1][2], 3))+" & "+str(round(resultArray[2][2], 3))+" & "+str(TagCount[2])+" & "+str(allTags["B-LOC_TP"])+" & "+str(allTags["B-LOC_FP"])+" & "+str(allTags["B-LOC_FN"])+" & "+str(GoldTags["B-LOC"])+"\\\\\\cline{2-9}")
	print("I-LOC & "+str(round(resultArray[0][3], 3))+" & "+str(round(resultArray[1][3], 3))+" & "+str(round(resultArray[2][3], 3))+" & "+str(TagCount[3])+" & "+str(allTags["I-LOC_TP"])+" & "+str(allTags["I-LOC_FP"])+" & "+str(allTags["I-LOC_FN"])+" & "+str(GoldTags["I-LOC"])+"\\\\\\cline{2-9}")
	print("B-ORG & "+str(round(resultArray[0][4], 3))+" & "+str(round(resultArray[1][4], 3))+" & "+str(round(resultArray[2][4], 3))+" & "+str(TagCount[4])+" & "+str(allTags["B-ORG_TP"])+" & "+str(allTags["B-ORG_FP"])+" & "+str(allTags["B-ORG_FN"])+" & "+str(GoldTags["B-ORG"])+"\\\\\\cline{2-9}")
	print("I-ORG & "+str(round(resultArray[0][5], 3))+" & "+str(round(resultArray[1][5], 3))+" & "+str(round(resultArray[2][5], 3))+" & "+str(TagCount[5])+" & "+str(allTags["I-ORG_TP"])+" & "+str(allTags["I-ORG_FP"])+" & "+str(allTags["I-ORG_FN"])+" & "+str(GoldTags["I-ORG"])+"\\\\\\cline{2-9}")
	print("B-MISC & "+str(round(resultArray[0][6], 3))+" & "+str(round(resultArray[1][6], 3))+" & "+str(round(resultArray[2][6], 3))+" & "+str(TagCount[6])+" & "+str(allTags["B-MISC_TP"])+" & "+str(allTags["B-MISC_FP"])+" & "+str(allTags["B-MISC_FN"])+" & "+str(GoldTags["B-MISC"])+"\\\\\\cline{2-9}")
	print("I-MISC & "+str(round(resultArray[0][7], 3))+" & "+str(round(resultArray[1][7], 3))+" & "+str(round(resultArray[2][7], 3))+" & "+str(TagCount[7])+" & "+str(allTags["I-MISC_TP"])+" & "+str(allTags["I-MISC_FP"])+" & "+str(allTags["I-MISC_FN"])+" & "+str(GoldTags["I-MISC"])+"\\\\\\cline{2-9}")
	print("& & & & & & & &\\\\\\cline{2-9}")
	Anzahl_TP = 0
	Anzahl_FP = 0
	Anzahl_FN = 0
	for x in searchList:
		Anzahl_TP += allTags[x+"_TP"]
		Anzahl_FP += allTags[x+"_FP"]
		Anzahl_FN += allTags[x+"_FN"]
	print("Durchschnitt / Summe & "+str(round(average[0], 3))+" & "+str(round(average[1], 3))+" & "+str(round(average[2], 3))+" & "+str(TagCount[8])+" & "+str(Anzahl_TP)+" & "+str(Anzahl_FP)+" & "+str(Anzahl_FN)+" & "+str(GoldTags["Gesamt"])+"\\\\\\cline{2-9}\n")
	
	print("SemEval'13 Metriken:")
	print("& COR & "+str(resultMeasures[0][0])+" & "+str(resultMeasures[1][0])+" & "+str(resultMeasures[2][0])+" & "+str(resultMeasures[3][0])+"\\\\\\cline{3-6}")
	print("& INC & "+str(resultMeasures[0][1])+" & "+str(resultMeasures[1][1])+" & "+str(resultMeasures[2][1])+" & "+str(resultMeasures[3][1])+"\\\\\\cline{3-6}")
	print("& PAR & "+str(resultMeasures[0][2])+" & "+str(resultMeasures[1][2])+" & "+str(resultMeasures[2][2])+" & "+str(resultMeasures[3][2])+"\\\\\\cline{3-6}")
	print("& MIS & "+str(resultMeasures[0][3])+" & "+str(resultMeasures[1][3])+" & "+str(resultMeasures[2][3])+" & "+str(resultMeasures[3][3])+"\\\\\\cline{3-6}")
	print("& SPU & "+str(resultMeasures[0][4])+" & "+str(resultMeasures[1][4])+" & "+str(resultMeasures[2][4])+" & "+str(resultMeasures[3][4])+"\\\\\\cline{3-6}")
	print("& Präzision & "+str(round(resultMeasures[0][5], 3))+" & "+str(round(resultMeasures[1][5], 3))+" & "+str(round(resultMeasures[2][5], 3))+" & "+str(round(resultMeasures[3][5], 3))+"\\\\\\cline{3-6}")
	print("& Recall & "+str(round(resultMeasures[0][6], 3))+" & "+str(round(resultMeasures[1][6], 3))+" & "+str(round(resultMeasures[2][6], 3))+" & "+str(round(resultMeasures[3][6], 3))+"\\\\\\cline{3-6}")
	print("& F1-Score & "+str(round(resultMeasures[0][7], 3))+" & "+str(round(resultMeasures[1][7], 3))+" & "+str(round(resultMeasures[2][7], 3))+" & "+str(round(resultMeasures[3][7], 3))+"\\\\\\cline{3-6}")
### ruft die Sequenzierungsmethode main(x,y) mit den Listen-Dateien der Tagger 1 und Tagger 2 auf
main(TextList1, TextList2)

### falls bugs/nomatch in main
#Fall_Counter()

### rufe alle restlichen relevanten Methoden in der richtigen Reihenfolge auf
countGold(TextList2)
calculateResults()
printResult()

print("Missing-Fälle:")
print_Metric(List_MIS)
print("Spurious-Fälle:")
print_Metric(List_SPU)
printforlatex()

### Gezählte und absteigend sortierte Wortlisten
print_word_count(TextList1)
print_word_count(TextList2)