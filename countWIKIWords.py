##############################################################
# Name: NbWords
# Purpose: This modeule is designed to build an index of the
#          number of words in each file from the WIKI collection
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import os
from parseCollection import *
from parseWIKI import normalize_wiki


if __name__ == "__main__":
    counts = {}
    for elem in os.listdir("../Wiki"):
        print(elem)
        for i, filename in enumerate(os.listdir("../Wiki/" + elem)):
            if (i % 1000 == 0):
                print ("%.2f%%" % (100. * i / 660000))
            clean_file = normalize_wiki(open("../Wiki/" + elem + "/" + filename, "r").read())
            counts[filename] = len(clean_file)

    with open("../WIKIindexes/finalWiki/countWords.json", "w") as dump:
        dump.write(json.dumps(counts, indent=2))
