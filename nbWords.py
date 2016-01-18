import os
from xml.etree import ElementTree
import unicodedata
from main import *

from parseXML import normalize_wiki


counts = {}
for elem in os.listdir("../wiki"):
    print(elem)
    for i, filename in enumerate(os.listdir("../wiki/" + elem)):
        if (i % 1000 == 0):
            print ("%.2f%%" % (100.*i/660000))
        clean_file = normalize_wiki(open("../wiki/" + elem + "/" + filename, "r").read())
    	counts[filename] = len(clean_file)



with open("counts.json", "w") as dump:
    dump.write(json.dumps(counts,  indent=2))