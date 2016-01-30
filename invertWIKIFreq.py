##############################################################
# Name: InvertJson
# Purpose: This modeule is designed to build inverse frequency dictionaries
#          from frequency dictionaries (for the WIKI collection)
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import os
import json

if __name__ == "__main__":
    for elem in os.listdir("../WIKIindexes/wikifreq"):
        print(elem)
        invertFreq = {}
        for i, filename in enumerate(os.listdir("../WIKIindexes/wikifreq/" + elem)):
            name = filename.split(".")[0]
            with open("../WIKIindexes/wikifreq/" + elem + "/" + filename, "r") as freq:
                frequencies = json.loads(freq.read())
                for word in frequencies:
                    if word not in invertFreq:
                        invertFreq[word] = [(name, frequencies[word])]
                    else:
                        invertFreq[word] += [(name, frequencies[word])]
            if ((i + 1) % 10000 == 0):
                print(i)
                with open("../WIKIindexes/invwiki/revert" + "-" + elem + "-" + str(i / 10000) + ".json", "w") as rev:
                    rev.write(json.dumps(invertFreq, indent=2))
                    rev.flush()
                invertFreq = {}
    if invertFreq:
        with open("../WIKIindexes/invwiki/revert" + "-" + elem + "-" + str(i / 10000) + ".json", "w") as rev:
            rev.write(json.dumps(invertFreq, indent=2))
            rev.flush()
