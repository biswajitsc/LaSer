# coding: utf-8

from lxml import etree
from StringIO import *
from lxml import objectify
import sympy

def parseMML(mmlinput):
	mmlinput= mmlinput.replace(' xmlns="', ' xmlnamespace="')
	parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
	tree   = etree.parse(StringIO(mmlinput), parser)
	objectify.deannotate(tree,cleanup_namespaces=True,xsi=True,xsi_nil=True)
	mmlinput=etree.tostring(tree.getroot())
	exppy="" #this is the python expression
	symvars=[]  #these are symbolic variables which can eventually take part in the expression
	events = ("start", "end")
	level = 0
	context = etree.iterparse(StringIO(mmlinput),events=events)
	for action, elem in context:
		if (action=='start') and (elem.tag=='mfrac'):
			level += 1
			mmlaux=etree.tostring(elem[0])
			(a,b)=parseMML(mmlaux)
			symvars.append(b)
			exppy+=a
			exppy+='/'
			mmlaux=etree.tostring(elem[1])
			(a,b)=parseMML(mmlaux)
			symvars.append(b)
			exppy+=a
		if (action=='end') and (elem.tag=='{http://www.w3.org/1998/Math/MathML}mfrac'):
			level -= 1
		if level:
			continue
		if (action=='start') and (elem.tag=='{http://www.w3.org/1998/Math/MathML}mrow'):
			exppy+='('
		if (action=='end') and (elem.tag=='{http://www.w3.org/1998/Math/MathML}mrow'):
			exppy+=')'
		if elem.text == None :
			continue
		if action=='start' and elem.tag=='{http://www.w3.org/1998/Math/MathML}mn': #this is a number
			exppy+=elem.text
		if action=='start' and elem.tag=='{http://www.w3.org/1998/Math/MathML}mi': #this is a variable
			exppy+=elem.text
			symvars.append(elem.text) #we'll return the variable, so sympy can sympify it afterwards
		if action=='start' and elem.tag=='{http://www.w3.org/1998/Math/MathML}mo': #this is a operation
			exppy+=elem.text
	return (exppy, symvars)

def main() :
	in_file = open("../../Data/MathML.xml","r")
	in_meta_file = open("../../Data/MathMLMeta.xml","r")
	out_file = open("../../Data/Expressions","w")
	output_file = open("../../Data/SimplifiedMathML","w")
	out_meta_file = open("../../Data/SimplifiedMathMLMeta","w")
	data = in_file.read()
	metadata = in_meta_file.read()
	mathml_eqns = data.split('\n')
	metadata_eqns = metadata.split('\n')
	i = 0
	for mathml_eqn in mathml_eqns :
		if (str(mathml_eqn) == '<?xml version="1.0" encoding="UTF-8"?>' or len(mathml_eqn) == 0) :
			continue
		mathml_eqn = mathml_eqn.replace('\n',' ')
		temp_mathml_eqn = mathml_eqn
		if (i % 100 == 0) :
			print i, 'done'
		try :
			mathml_eqn = mathml_eqn.replace("<m:mo><U+2062></m:mo>","")
			(expr, symbvars) = parseMML(mathml_eqn)
			simp_expr = sympy.simplify(expr)
			out_file.write(str(expr) + '\n$$\n$$\n' + str(simp_expr) + '\n')
			c_mathml = sympy.printing.mathml(simp_expr)
			from sympy.utilities.mathml import c2p
			p_mathml = c2p(c_mathml)
			p_mathml = str(p_mathml)
			p_mathml = p_mathml.replace('\n',' ')
			output_file.write(str(temp_mathml_eqn) + '\n' + p_mathml + '\n')
			out_meta_file.write(str(metadata_eqns[i]) + " " + str(i + 1) + '\n' + str(metadata_eqns[i]) + " " + str(i + 1) + '\n')
		except Exception :
			output_file.write(str(temp_mathml_eqn) + '\n')
			out_meta_file.write(str(metadata_eqns[i]) + " " + str(i + 1) + '\n')
		i += 1

	in_file.close()
	out_file.close()

if __name__ == "__main__" :
	main()