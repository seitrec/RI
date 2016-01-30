##############################################################
# Name: MergeTotal
# Purpose: This modeule is supposed to merge all partial indexes to have a final
#          one containing all the data (I had to try... but even 16Gigs of RAM isn't enough !
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import os
import json

if __name__ == "__main__":
    final_dict = {}
    for j, filename in enumerate(os.listdir("../WIKIindexes/finalWiki/")):
        print(j)
        with open("../WIKIindexes/finalWiki/" + filename, "r") as f:
            part = json.loads(f.read())
            final_dict.update(part)
    with open("../WIKIindexes/Wiki/invWiki.json", "w") as dump:
        dump.write(json.dumps(final_dict, indent=2))
