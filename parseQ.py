import argparse
from main import *
import vectoriel

def parseQueries():
	with open("../CACM/query.text", "r") as cacm:
		collection = cacm.read()
		with open("../CACM/common_words", "r") as cw:
			common_words = replacePunct(cw.read())
			files = [item.split("\n.") for item in collection.split(".I ")]
			return files

def main(collection):
	queries = parseQueries()
	parts = {item[0].rstrip(): list(itertools.chain(*([replacePunct(line[1:])
													  for line in item[1:]
													  if line[0] =="W"])))
			for item in queries}
	for index, qu in parts.iteritems():
		print(collection, index, " ".join(qu))
		yield (index, qu, vectoriel.main(collection, " ".join(qu)))




if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Query CACM or WIKI and get vectorial results")
	parser.add_argument("-c", "--collection", default="CACM", help="The collection we want to query from")
	args = parser.parse_args()
	print main(args.collection)