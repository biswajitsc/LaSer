from convertMathMLExpression import convertEquation
mathML = []
with open('../../Data/MathML.xml','r') as f:
	for line in f:
		mathML.append(line)
		break
print mathML
convertEquation(mathML)