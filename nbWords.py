##############################################################
# Name: NbWords
# Purpose: This modeule is designed to build an index of the
#          number of words in each file from the WIKI collection
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import os
from parseCollection import *
from parseXML import normalize_wiki

counts = {}
for elem in os.listdir("../wiki"):
    print(elem)
    for i, filename in enumerate(os.listdir("../wiki/" + elem)):
        if (i % 1000 == 0):
            print ("%.2f%%" % (100. * i / 660000))
        clean_file = normalize_wiki(open("../wiki/" + elem + "/" + filename, "r").read())
        counts[filename] = len(clean_file)

with open("counts.json", "w") as dump:
    dump.write(json.dumps(counts, indent=2))
