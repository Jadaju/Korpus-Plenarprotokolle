import spacy
import codecs
from collections import Counter
from spacy_conll import ConllFormatter
import stanza
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
import re

with codecs.open('F:/Dropbox/Master/Plenarprotokolle/Preprocessing/09036-f.txt', 'r', 'utf-8') as myfile:
  data = myfile.read()

#"leichteres" Model
#nlp = spacy.load("de_core_news_sm")

#"schwereres"Model
nlp = spacy.load("de_core_news_md")

conllformatter = ConllFormatter(nlp)
nlp.add_pipe(conllformatter, after='parser')

doc = nlp(data)

#json_doc = doc.to_json()


#print(doc[0].ent_iob_+"-"+doc[0].ent_type_)

newfile = open(r"F:\Dropbox\Master\SpacyZuConll.conll","w+", encoding="utf-8")


counter = 1
for x in doc:
	#ent_san = [doc[x].text, doc[x].ent_iob_, doc[x].ent_type_]
	#print(ent_san)
	if re.findall('\r', x.text) == []:
		if x.ent_iob_ != "O":
			newfile.write(str(counter)+"	"+x.text+"	"+"_"+"	"+"_"+"	"+x.ent_iob_+"-"+x.ent_type_+"	"+"_"+"	"+"_"+"\n")
		else:
			newfile.write(str(counter)+"	"+x.text+"	"+"_"+"	"+"_"+"	"+x.ent_iob_+x.ent_type_+"	"+"_"+"	"+"_"+"\n")
		counter += 1
	else:
		newfile.write("\n")
		counter = 1

#print(doc._.conll_str)
#print(doc.sents)

#nlp.to_disk(r"C:\Users\Flopf\Documents")
#doc.to_disk(r"F:")


# for ent in doc.ents:
    # #print(ent.text, ent.label_)
	# print(ent, ent.label_)
	

# labels = [x.label_ for x in doc.ents]
# print(Counter(labels))

# sentences = [x for x in doc.sents]
# print(len(sentences))

newfile.close()







#print(json_doc)

# with open(r"F:\Dropbox\Master\SpacyZuJson.json","w+", encoding="utf-8") as newfile:


	# print(json_doc, file = newfile)
# #print(doc._.conll_str)
# #print(doc.sents)

# #nlp.to_disk(r"C:\Users\Flopf\Documents")
# #doc.to_disk(r"F:")


# # for ent in doc.ents:
    # # #print(ent.text, ent.label_)
	# # print(ent, ent.label_)
	

# # labels = [x.label_ for x in doc.ents]
# # print(Counter(labels))

# # sentences = [x for x in doc.sents]
# # print(len(sentences))

# newfile.close()