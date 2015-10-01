import sys
import re
import os
import codecs

windowSize = 10

def parse(line):
    line = line.replace(',', ' ')
    tokens = line.split()
    res = []
    isSymbol = [False for x in range(len(tokens))]
    for i in xrange(0, len(tokens)):
        if tokens[i].startswith('$') and tokens[i].endswith('$'):
            if (tokens[i].count('$') == 2):
                isSymbol[i] = True

    for i in xrange(0, len(tokens)):
        if isSymbol[i]:
            before = ""
            for j in xrange(1, windowSize):
                if i - j < 0 or tokens[i - j].startswith('\\end'):
                    break
                if not isSymbol[i - j]:
                    before = tokens[i - j] + ' ' + before
            before = before[:-1]
            after = ""
            for j in xrange(1, windowSize):
                if i + j >= len(tokens) or tokens[i + j].startswith('\\begin'):
                    break
                if not isSymbol[i + j]:
                    after += tokens[i + j] + ' '
            after = after[:-1]
            res.append((before, tokens[i], after))
    return res

def main():
    skipped = 0
    cnt = 0

    for year in reversed(xrange(1992, 2004)):

        print 'Processing year {0}'.format(year)
        files = os.listdir('../../Dataset/{0}'.format(year))
        for afile in files:
            cnt += 1
            out = open('../../Data/Context/' + afile, 'w')
            if cnt % 100 == 0:
                print "Done ", cnt, "Skipped ", skipped

            try:
                data = open('../../Dataset/{0}/{1}'.format(year, afile), 'r').read().decode('cp1252', errors='ignore')
                lines = data.split('\n')
                data = ""
                for line in lines:
                    if (line.startswith('%')):
                        continue
                    data += '\n' + line

                lines = re.compile('\.\s+').split(data);
                
                for line in lines:
                    res = parse(line)
                    for entry in res:
                        try:
                            out.write(entry[0] + ' ' + entry[1] + ' ' + entry[2] + '\n')
                        except:
                            continue
                
                out.close()

            except Exception as obj:
                print year, afile
                print obj
                raise
    

if __name__ == '__main__':
    main()