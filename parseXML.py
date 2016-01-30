##############################################################
# Name: parseXML
# Purpose: This modeule is designed to parse XML files in order
#          to keep only the real content
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import os
from xml.etree import ElementTree
import unicodedata
from parseCollection import *


def normalize_wiki(open_file):
    xml_free = ''.join(ElementTree.fromstring(open_file).itertext())
    if type(xml_free) == unicode:
        xml_free = unicodedata.normalize('NFKD', xml_free).encode('ascii', 'ignore')
    clean_file = replacePunct(xml_free)
    return clean_file


if __name__ == "__main__":
    for elem in os.listdir("../wiki"):
        print(elem)
        for i, filename in enumerate(os.listdir("../wiki/" + elem)):
            if (i % 1000 == 0):
                print ("%.2f%%" % (100. * i / 660000))
            clean_file = normalize_wiki(open("../wiki/" + elem + "/" + filename, "r").read())
            with open("../CACM/common_words", "r") as cw:
                common_words = replacePunct(cw.read())
                freq = count_words(common_words, clean_file)
                dump_dir_path = "../wikifreq/" + elem + "/"
                if not os.path.exists(dump_dir_path):
                    os.makedirs(dump_dir_path)
                with open(dump_dir_path + filename.split(".")[0] + ".json", "w") as dump:
                    dump.write(json.dumps(freq, indent=2))
