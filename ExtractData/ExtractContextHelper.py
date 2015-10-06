import sys
import re


			
def main():
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
					commandname = re.sub('[\[#].*','',m.group(1))
					text = m.group(2)
					print commandname,' ',text
				except Exception as e:
					continue
			elif p2.match(line_) is not None:
				# print line_
				try:
					m = re.match("^\\\\r?e?newcommand{(.*)}(\[\d+\])?(\[.*\])?{(.*)}$", line_)
					# print \
					# [\
					# m.group(1),\
					# m.group(2),\
					# m.group(3),\
					# m.group(4)\
					# ]

					if m.group(1) is not None:
						commandname = m.group(1)
					if m.group(2) is not None:
						numargs = int((m.group(2)).strip().strip('[').strip(']').strip())
					if m.group(3) is not None:
						firstargval = m.group(3).strip().strip('[').strip(']').strip()
					if m.group(4) is not None:
						text = m.group(4)
					print commandname,' ',text
				except Exception as e:
					continue
				
				# elif p3.match(line_) is not None:
					
				# break


	# print temp


if __name__ == '__main__':
	main()