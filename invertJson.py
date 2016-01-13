import os
import json

invertFreq = {}

for elem in os.listdir("../wikifreq"):
	print(elem)
	for i, filename in enumerate(os.listdir("../wikifreq/" + elem)):
		name = filename.split(".")[0]
		if (i % 1000 == 0):
			print(i)
		with open("../wikifreq/" + elem + "/" + filename, "r") as freq:
			frequencies = json.loads(freq.read())
			for word in frequencies:
				if word not in invertFreq:
					invertFreq[word] = [(name, frequencies[word])]
				else:
					invertFreq[word] += [(name, frequencies[word])]

with open("../invwiki/revertFreq.json", "w") as rev:
	rev.write(json.dumps(invertFreq, indent=2))