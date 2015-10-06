import sys
import re


			
def main():
	temp = {}
	prev = ''
	with open(sys.argv[1], 'r') as f:
		for line in f:
			line_ = line.strip().strip('\n').strip()
			p1 = re.compile("^(\\\\def)(.*)$")
			p2 = re.compile("^(\\\\newcommand)(.*)$")
			p3 = re.compile("^(\\\\let)(.*)$")
			if p1.match(line_) is not None: 
				# print line_
				try:
					m = re.match("^\\\\def([^{]*){(.*)}$", line_)
					temp[m.groups(1)] = m.groups(2)
					print [m.group(1),m.group(2)]
				except Exception as e:
					continue
			elif p2.match(line_) is not None:
				# print line_
				try:
					m = re.match("^\\\\newcommand{(.*)}(\[\d+\])?{(.*)}$", line_)
					temp[m.groups(1)] = m.groups(3)
					print [m.group(1),m.group(3)]
				except Exception as e:
					continue
				
				# elif p3.match(line_) is not None:
					
				# break


	# print temp


if __name__ == '__main__':
	main()