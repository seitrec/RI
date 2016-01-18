import os
import json

if __name__ == "__main__":
	final_dict = {}
	for j, filename in enumerate(os.listdir("../finalWiki/")):
		print(j)
		with open("../finalWiki/" + filename, "r") as f:
			part = json.loads(f.read())
			final_dict.update(part)
	with open("../Wiki/invWiki.json", "w") as dump:
		dump.write(json.dumps(final_dict, indent = 2))