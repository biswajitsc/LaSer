# coding: utf-8
import re
import decimal
import sys
import unicodedata as ucode

def numberNormalize(data) : 
    lines = data.split('\n')
    # lines = ['<mn>2.45</mn>   <m:mn>2.45646</m:mn> <mn>2</mn>   <mn>2.45</mn>']
    normalizedLines = []
    for line in lines :
        matches = re.findall(r'<mn>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?</mn>', line)
        already_matched = set()
        normalizedLines.append(line)
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
                        normalizedLines.append(temp_line)
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
                        normalizedLines.append(temp_line)
                        i += 1
                                
    return normalizedLines

map = {}

def initMap():
    fileName = "operator_groups.txt"
    data = open(fileName,'r').read()
    tokens = data.split('\n')
    id = 1

    for token in tokens:
        # print token
        operators = token.split(' ')
        for c in operators:
            map[c] = "OP" + str(id)
        id += 1

    # for key in map:
    #     print key, map[key]

def addGroups(data):
    normalized = ''
    lines = data.split('\n')

    for line in lines:
        tokens = line.split(' ')
        for token in tokens:
            s1 = '<m:mo>'
            e1 = '</m:mo>'
            s2 = '<mo>'
            e2 = '</mo>'
            found = False
            if token.startswith(s1):
                st = token.find(s1) + len(s1)
                en = token.find(e1)
                op = token[st:en]
                if (op in map):
                    normalized += token + s1 + map[op] + e1
                    found = True
            elif token.startswith('<mo>'):
                st = token.find(s2) + len(s2)
                en = token.find(e2)
                op = token[st:en]
                if (op in map):
                    normalized += token + s2 + map[op] + e2
                    found = True

            if not found:
                normalized += token

            normalized += ' '
        normalized += '\n'
    return normalized

def operatorNormalize(data):
    initMap()
    return addGroups(data)

def unicodeNormalize(data) :
    lines = data.split('\n')
    normalizedString = ""
    for line in lines:
        tokens = line.split(' ')
        for token in tokens:
            startTag = '<m:mi>';
            endTag = '</m:mi>'
            normalized = False
            for iter in range(2):
                if (token.startswith(startTag)):
                    st = token.find(startTag) + len(startTag)
                    en = token.find(endTag)
                    symbol = unicode(token[st:en], "utf-8")
                    symbol = ucode.normalize('NFKD', symbol)
                    symbol = symbol.encode('ascii', 'backslashreplace')
                    normalizedString += startTag + symbol + endTag
                    normalized = True
                    break
                startTag = '<mi>'
                endTag = '</mi>'
            if not normalized:
                normalizedString += token

            normalizedString += ' '
        normalizedString += '\n'

    return normalizedString

def main():
    numArgs = len(sys.argv)
    if (numArgs != 2):
        print "Usage: python Normalization.py filename"
        sys.exit();

    fileName = sys.argv[1]
    data = open(fileName,'r').read()

    # Unicode Normalization (Disabled for now)
    unicode_normalized = data
    # unicode_normalized = unicodeNormalize(data)

    # Operator Grouping
    operator_normalized = operatorNormalize(unicode_normalized)

    print operator_normalized
    
    # Number Normalization
    number_normalized = numberNormalize(operator_normalized)

    # print number_normalized

if __name__ == '__main__':
    main()