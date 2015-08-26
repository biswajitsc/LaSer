from lxml import etree
from StringIO import *
import re
import sys

def main() :
	input_file = open(sys.argv[1],"r")
	data = input_file.read()
	data = data.replace("\n"," ")
	lines = data.split('<m:math')
	mathML = []
	for line in lines :
		line = line.replace('\n', ' ')
		if len(line) == 0 :
			continue
		line = '<m:math' + line
		xml = line.split('<?xml version="1.0"?>')
		for xmls in xml :
			xmls = re.sub(' +',' ',xmls)
			xmls = xmls.replace('\t', ' ')
			mathML.append(xmls)
	
	for eqn in mathML :
		try :
			string = eqn.replace(' xmlns="', ' xmlnamespace="')
			parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
			tree   = etree.parse(StringIO(string), parser)
			root = tree.getroot()
			tags = root.findall('.//')
			strng = ""
			for tag in tags :
				if len(tag.text) == 0 :
					continue
				text = tag.text.strip()
				if len(text) != 0 :
					strng += text + " "
			print strng
		except Exception :
			continue

if __name__ == "__main__" :
	main()