##############################################################
# Name: MergeAlpha
# Purpose: This module is designed to merge partial inverse frequency indexes
#          together, to have a final state of 678 indexes (26*26 for the alphabetical,
#          one numerical, and one for others)
# Important Note: In the end we basically just dropped the digits, 
# because they were too big a part, weren't really usefull, and 
# we wouldn't take the time to split them again...
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import os
import json

if __name__ == "__main__":
    for i, dirname in enumerate(os.listdir("../invwikialpha/")):
        # Yup, 678 folders, 26*26 + 2
        print "%s/677" % i, dirname
        final_dict = {}
        for j, filename in enumerate(os.listdir("../invwikialpha/" + dirname)):
            print "%s/64" % j, filename
            with open("../invwikialpha/" + dirname + "/" + filename, "r") as f:
                part = json.loads(f.read())
                for key, value in part.iteritems():
                    if key in final_dict:
                        final_dict[key] += value
                    else:
                        final_dict[key] = part[key]
        with open("../finalWiki/" + dirname + ".json", "w") as dump:
            dump.write(json.dumps(final_dict, indent=2))
