import sys
import re


			
def main():
	with open(sys.argv[1], 'r') as f:
		for line in f:
			line_ = line.strip().strip('\n').strip()
			p1 = re.compile("^(\\\\def)(.*)$")
			p2 = re.compile("^(\\\\newcommand)(.*)$")
			p3 = re.compile("^(\\\\let)(.*)$")
			if p1.match(line_) is not None or p2.match(line_) is not None or p3.match(line_) is not None:
				print line_
			# break


if __name__ == '__main__':
	main()