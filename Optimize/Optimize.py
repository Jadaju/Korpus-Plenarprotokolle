import codecs
import re
import wikipedia
import requests
from bs4 import BeautifulSoup

### lies Dateien ein
fileone = codecs.open("F:/Dropbox/Master/Plenarprotokolle/Annotiert/Optimierung/MDB_STAMMDATEN.XML", "r", "utf-8")

### Dateien zu Strings
TextString1 = fileone.read()

TextList1 = TextString1.splitlines()

wikipedia.set_lang("de")

crawl = []
crawl2 = []

def crawl_wikipedia():

	for wp in range(1, 20):
		custom_stuff = wikipedia.page("Bundestagsausschüsse des "+str(wp)+". Deutschen Bundestages")
		custom_stuff = custom_stuff.html().splitlines()

		for x in custom_stuff:
			if "Ausschuss" in x or re.findall("ausschuss", x) != []:
				if re.findall(">.+</a>$", x) != []:
					#print(x)
					a = re.sub("<br />", "", x)
					a = re.sub(".+>(.+)</a>$", r"\1", a)
					title = re.sub(".+title=\"(.+)\">.+", r"\1", x)
					#print("a:	"+a)
					#print("title:	"+title)
					if a not in crawl:
						crawl.append(a)
					if title not in crawl:
						crawl.append(title)
				elif re.findall("<small", x) != []:
					#print("WP:	"+str(wp))
					#print(x)
					if re.findall("title=\"", x):
						title = re.sub(".+title=\"(.+)\">.+", r"\1", x)
						#print("title2:	"+title)
						if title not in crawl:
							crawl.append(title)
					a = re.sub("<br />", "", x)
					a = re.sub("<a href=.+\">", "", a)
					a = re.sub("<td>", "", a)
					a = re.sub("</a>", "", a)
					a = re.sub("<small>.+</small>(.+)<small>.+</small>", r"\1 < >", a)
					a = re.sub("<.+>", "SPLIT", a)
					a = a.split("SPLIT")
					for y in a:
						if y != "":
							#print("y:	"+y)
							if y not in crawl:
								crawl.append(y)
				elif re.findall("^<td>.+", x) !=[]:
					#print("WP:	"+str(wp))
					#print(x)
					a = re.sub("<br />", "", x)
					a = re.sub("<td>", "", a)
					a = re.sub("  ", " ", a)
					a = re.sub("<sup id=.+", " ", a)
					a = re.sub("<a href=.+\">", "", a)
					a = re.sub("</a>", "", a)
					if a not in crawl:
						crawl.append(a)
					#print("a:	"+a)
				else:
					#print("WP:	"+str(wp))
					#print("REST:	"+x)
					pass

	i = 0
	for x in crawl:
		i += 1
		korrektur = re.sub("  ", " ", x)
		korrektur = re.sub("\(Seite nicht vorhanden\)", "", korrektur)
		crawl[i-1] = korrektur
		#print(str(i)+":	"+korrektur)


def crawl_wikipedia_2():
	url = "https://de.wikipedia.org/wiki/Bundesministerium_(Deutschland)"
	r = requests.get(url)
	r.encoding = "utf-8"
	#custom_stuff2 = wikipedia.page("Bundesministerium (Deutschland)")
	#custom_stuff2 = custom_stuff2.html()
	soup = BeautifulSoup(r.content, "html.parser")
	#print()
	table = soup.find_all("table", class_ = "wikitable sortable zebra")
	
	#print(table)
	
	for table_body in table[0].find_all("tbody"):
		rows = table_body.find_all("td")
		#print(rows)
		count = 0
		it = 1
		for row in rows:
			if it == 2 or it == 3:
				count += 0.5
				#print(str(count)+":	"+row.text)
				crawl2.append(row.text)
			elif it == 9:
				it = 0
			it += 1
	for table_body in table[1].find_all("tbody"):
		rows = table_body.find_all("td")
		#print(rows)
		count = 0
		it = 1
		for row in rows:
			if it == 1:
				count += 1
				#print(str(count)+":	"+row.text)
				sub = re.sub("\n", "", row.text)
				#print(sub)
				crawl2.append(sub)
			elif it == 4:
				it = 0
			it += 1
	#print(crawl2)

gazetteer = {
		"PER": [],
		"LOC": [],
		"ORG": [],
		"MISC": []
		}

###add custom Token
def add_custom():
	customPER = ["Trump"]
	for x in customPER:
		gazetteer["PER"].append(x)
	customLOC = ["Zonenrandgebiet", "Zonenrandregion", "Bundesrepublik", "Europa", "Großbritannien", "Euro-Zone", "Vereinigte Königreich"]
	for x in customLOC:
		gazetteer["LOC"].append(x)
	customORG = ["Bundesumweltamt", "Bundeskriminalamt, ""Verfassungsgericht", "Bundesgesundheitsamt", "BMJFG", "Bundeszentrale für gesundheitliche Aufklärung", "Bundeszentrale für politische Bildung", "Bund", "BÜNDNISSES 90/DIE GRÜNEN", "DIE LINKE", "CDU/CSU", "Bundeswehr", "Bundesregierung", "Ältestenrat", "Fraktion der SPD", "SPD-Fraktion", "Fraktion der CDU/CSU", "CDU/CSU-Fraktion", "CDU/CSU/DSU-Fraktion", "Fraktion der CDU/CSU/DSU", "Fraktion der AfD", "AfD-Fraktion", "Fraktion der FDP", "FDP-Fraktion", "Fraktion Die Linke", "Fraktion DIE LINKE", "Linksfraktion", "Gruppe der PDS", "PDS-Fraktion", "Fraktion der PDS", "Fraktion Bündnis 90/Die Grünen", "Fraktion die Grünen", "Fraktion die Grünen/Bündnis 90", "Gruppe Bündnis 90/Die Grünen", "DP-Fraktion", "DP/DPB-Fraktion", "DP-Gruppe", "FVP-Bundestagsfraktion", "Arbeitsgemeinschaft Freier Demokraten", "Demokratische Arbeitsgemeinschaft", "KPD-Fraktion", "Gruppe der KPD", "Fraktion der Föderalistischen Union", "Fraktion des Zentrums", "BP-Fraktion", "WAV-Fraktion", "Gruppe der WAV", "GB/BHE-Fraktion", "Deutscher Gemeinschaftsblock der Heimatvertriebenen und Entrechteten", "Gruppe Nationale Rechte", "Gruppe Kraft/Oberländer"]
	for x in customORG:
		gazetteer["ORG"].append(x)
	customMISC = ["Grundgesetz", "EWG-Vertrag", "Brexit", "Grexit", "Holocaust", "Agenda 2010", "Kerneuropa"]
	for x in customMISC:
		gazetteer["MISC"].append(x)

###add crawled data
def add_crawls():
	for x in crawl:
		if x in gazetteer["ORG"]:
			pass
		elif re.findall("^ ", x) != []:
			sub = re.sub("^ ", "", x)
			gazetteer["ORG"].append(x)
			#print("JA:"+sub)
		else:
			gazetteer["ORG"].append(x)
			#print("NE:"+x)
	for x in crawl2:
		if x in gazetteer["ORG"]:
			pass
		else:
			#print(x)
			gazetteer["ORG"].append(x)

### do add crawl
crawl_wikipedia()
crawl_wikipedia_2()
add_crawls()

add_custom()

def add_oldSpelling():
	for x in gazetteer["ORG"]:
		if re.findall("Ausschuss ", x) != [] or re.findall("ausschuss ", x) != []:
			#print("x:	"+x)
			old = re.sub("Ausschuss ", "Ausschuß ", x)
			#print("old1:	"+old)
			old = re.sub("ausschuss ", "ausschuß ", old)
			#print("old2:	"+old)
			if old not in gazetteer["ORG"]:
				gazetteer["ORG"].append(old)

def build_gazetteer():
	
	#Filepath = "F:\Dropbox\Master\Plenarprotokolle\Annotiert\Optimierung\WP"+str(
	newfile = open(r"F:\Dropbox\Master\Plenarprotokolle\Annotiert\Optimierung\regexner.txt","w+", encoding="utf-8")
	
	for x in TextList1:
		line = x
		line = re.sub("^ +", "", line)
		### PERSONS
		if re.findall("<NACHNAME>", line) != [] or re.findall("<VORNAME>", line) != []:
			line = re.sub("^<.+>(.+)</.+>$", r"\1", line)
			if line in gazetteer["PER"]:
				pass
			else:
				gazetteer["PER"].append(line)
		## LOCATIONS
		elif re.findall("<ORTSZUSATZ>", line) != [] or re.findall("<GEBURTSORT>", line) != [] or re.findall("<GEBURTSLAND>", line) != []:
			line = re.sub("^<.+>(.+)</.+>$", r"\1", line)
			#entfernt unnötige Klammern
			line = re.sub("^\((.+)\)$", r"\1", line)
			#entferne Klammern, die für Fehler sorgen
			line = re.sub("\(.+ .+\)$", "", line)
			#beachte Gemeindeänderungen, gekennzeichnet durch "jetzt" -> Bsp: A (jetzt B), fügt A und B zur Locations-Liste hinzu
			line = re.sub("jetzt ", "", line)
			line = re.sub("heute ", "", line)
			line = re.sub("ehem\. ", "", line)
			line2 = line.split(" / ")
			for x in line2:
				if x in gazetteer["LOC"]:
					pass
				else:
					gazetteer["LOC"].append(x)
		## ORGANIZATIONS
		elif re.findall("<PARTEI_KURZ>", line) != [] or re.findall("<INS_LANG>", line) != []:
			line = re.sub("^<.+>(.+)</.+>$", r"\1", line)
			#entfernt unnötige Klammern
			line = re.sub("^\((.+)\)$", r"\1", line)
			#entferne Klammern, die für Fehler sorgen
			line = re.sub("\(.+ .+\)$", "", line)
			if line in gazetteer["ORG"]:
				pass
			else:
				gazetteer["ORG"].append(line)

	add_oldSpelling()

	### write dictionary to file in RegexNER format
	for x in gazetteer["PER"]:
		newfile.write(x+"	PERSON\n")
	for x in gazetteer["LOC"]:
		if x == "Berlin":
			newfile.write(x+"	LOCATION	PERSON	1.0\n")
		else:
			newfile.write(x+"	LOCATION\n")
	for x in gazetteer["ORG"]:
		newfile.write(x+"	ORGANIZATION\n")
	for x in gazetteer["MISC"]:
		newfile.write(x+"	MISC\n")

	newfile.close()

build_gazetteer()

#print(gazetteer)