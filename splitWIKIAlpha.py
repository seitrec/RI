##############################################################
# Name: alphaSplit
# Purpose: This modeule is designed to breakdown inverse frequency dictionaries
#          to alphanumerial parts (based on the two first characters)
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################


import os
import json

if __name__ == "__main__":
    for i, filename in enumerate(os.listdir("../WIKIindexes/invwiki/")):
        alpha = {"0": {}, "_": {}}
        print("%s/67" % i)
        try:
            with open("../WIKIindexes/invwiki/" + filename, "r") as inv:
                basic = json.loads(inv.read())
                for word in basic:
                    pre = word[0:2]
                    try:
                        if pre.isdigit():
                            alpha["0"][word] = basic[word]
                        elif pre.isalpha():
                            if pre not in alpha:
                                alpha[pre] = {}
                            alpha[pre][word] = basic[word]
                        else:
                            alpha["_"][word] = basic[word]
                    except KeyError:
                        print word
                        pass
        except ValueError:
            print filename
        for pre in alpha:
            dump_dir_path = "../WIKIindexes/invwikialpha/" + pre + "/"
            if not os.path.exists(dump_dir_path):
                os.makedirs(dump_dir_path)
            with open(dump_dir_path + filename, "w") as dump:
                dump.write(json.dumps(alpha[pre], indent=2))
