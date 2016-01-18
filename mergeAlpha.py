import os
import json

if __name__ == "__main__":
	for i, dirname in enumerate(os.listdir("../invwikialpha/")):
		print("%s/28" % i)
		final_dict = {}
		for j, filename in enumerate(os.listdir("../invwikialpha/" + dirname)):
			with open("../invwikialpha/" + dirname + "/" + filename, "r") as f:
				part = json.loads(f.read())
				print(j)
				for key, value in part.iteritems():
					if key in final_dict:
						final_dict[key] += value
					else:
						final_dict[key] = part[key] 
		with open("../finalWiki/" + dirname + ".json", "w") as dump:
			dump.write(json.dumps(final_dict, indent = 2))