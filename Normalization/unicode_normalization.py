import unicodedata as ucode
import sys

numArgs = len(sys.argv)
if (numArgs != 2):
    print "Format python unicode_normalization.py filename"
    sys.exit();

fileName = sys.argv[1]
data = open(fileName,'r').read()
normalized = ''
tokens = data.split()
for token in tokens:
    if (token.startswith('<m:mi>')):
       st = token.find('<m:mi>') + 6
       en = token.find('</m:mi>')
       symbol = unicode(token[st:en], "utf-8")
       symbol = ucode.normalize('NFKD', symbol)
       symbol = symbol.encode('ascii', 'backslashreplace')
       print token
    else:
        print token

