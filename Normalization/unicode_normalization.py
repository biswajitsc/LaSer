import unicodedata as ucode
import sys

numArgs = len(sys.argv)
if (numArgs != 2):
    print "Usage: python unicode_normalization.py filename"
    sys.exit();

fileName = sys.argv[1]
data = open(fileName,'r').read()
normalized = ''
tokens = data.split()
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
            print startTag + symbol + endTag
            normalized = True
            break
        startTag = '<mi>'
        endTag = '</mi>'
    if not normalized:
        print token

