# coding: utf-8
import re
import decimal

def main() :
	input_file = open("../../Data/SimplifiedMathML","r")
	output_file = open("../../Data/NumberNormalizedMathML","w")
	data = input_file.read()
	lines = data.split('\n')
	# lines = ['<mn>2.45</mn>   <m:mn>2.45646</m:mn> <mn>2</mn>   <mn>2.45</mn>']
	for line in lines :
		matches = re.findall(r'<mn>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?</mn>', line)
		already_matched = set()
		numberNormalizedLines = []
		numberNormalizedLines.append(line)
		for match in matches :
			if len(match) > 0 :
				if match[0] not in already_matched :
					already_matched.add(match[0])
					d = decimal.Decimal(match[0])
					exp = abs(d.as_tuple().exponent)
					i = 0
					orig_string = '<mn>' + str(match[0]) + '</mn>'
					while i < exp :
						strng = '<mn>' + str(round(d, i)) + '</mn>'
						temp_line = line.replace(orig_string, strng)
						numberNormalizedLines.append(temp_line)
						i += 1
		matches = re.findall(r'<m:mn>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?</m:mn>', line)
		already_matched = set()
		for match in matches :
			if len(match) > 0 :
				if match[0] not in already_matched :
					already_matched.add(match[0])
					d = decimal.Decimal(match[0])
					exp = abs(d.as_tuple().exponent)
					orig_string = '<m:mn>' + str(match[0]) + '</m:mn>'
					i = 0
					while i < exp :
						strng = '<m:mn>' + str(round(d, i)) + '</m:mn>'
						temp_line = line.replace(orig_string, strng)
						numberNormalizedLines.append(temp_line)
						i += 1
								
		for normalizedLine in numberNormalizedLines : 
			output_file.write(normalizedLine + '\n')
			# print normalizedLine
	input_file.close()
	output_file.close()

if __name__ == "__main__" :
	main()