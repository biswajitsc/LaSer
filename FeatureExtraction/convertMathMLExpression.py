from lxml import etree
from StringIO import *
import re
import sys

def convertEquation(mathML) :
	expressions = []
	j = 0
	for eqn in mathML :
		j += 1
		try :
			string = eqn.replace(' xmlns="', ' xmlnamespace="')
			parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
			tree   = etree.parse(StringIO(string), parser)
			root = tree.getroot()
			tags = root.findall('.//')
			strng = ""
			for tag in tags :
				if tag.text == None or len(tag.text) == 0 :
					continue
				text = tag.text.strip()
				if len(text) != 0 :
					strng += text + " "
			expressions.append(strng)
		except Exception as ex :
			print j, ex, len(eqn.split(' '))
			continue
	return expressions

if __name__ == "__main__" :
	main()