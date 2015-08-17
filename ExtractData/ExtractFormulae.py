import os
import re
import codecs

mmode0 = re.compile(r'\$\$.+?\$\$', flags = re.DOTALL | re.UNICODE)
mmode1 = re.compile(r'\$.+?\$', flags = re.DOTALL | re.UNICODE)
mmode2 = re.compile(r'\\\[.+?\\\]', flags = re.DOTALL | re.UNICODE)
mmode3 = re.compile(r'\\begin{equation}.+?\\end{equation}', flags = re.DOTALL | re.UNICODE)
mmode4 = re.compile(r'\\begin{eqnarray}.+?\\end{eqnarray}', flags = re.DOTALL | re.UNICODE)
mmode5 = re.compile(r'\\begin{equation\*}.+?\\end{equation\*}', flags = re.DOTALL | re.UNICODE)
mmode6 = re.compile(r'\\begin{eqnarray\*}.+?\\end{eqnarray\*}', flags = re.DOTALL | re.UNICODE)

def primary_processing(inp):
    inp = re.sub(r'.*\\newcommand.*', '', inp)
    
    s0 = mmode0.findall(inp)
    inp = mmode0.sub('', inp)

    s1 = mmode1.findall(inp)
    inp = mmode1.sub('', inp)

    s2 = mmode2.findall(inp)
    inp = mmode2.sub('', inp)

    s3 = mmode3.findall(inp)
    inp = mmode3.sub('', inp)

    s4 = mmode4.findall(inp)
    inp = mmode4.sub('', inp)
    
    s5 = mmode5.findall(inp)
    inp = mmode5.sub('', inp)
    
    s6 = mmode6.findall(inp)
    inp = mmode6.sub('', inp)

    ret = []
    
    [ret.append(i) for i in s0]
    [ret.append(i) for i in s1]
    [ret.append(i) for i in s2]
    [ret.append(i) for i in s3]
    [ret.append(i) for i in s4]
    [ret.append(i) for i in s5]
    [ret.append(i) for i in s6]
    
    return ret

def secondary_processing(inp):
    inp = inp.replace('\n',' ')
    
    if mmode0.match(inp) != None:
        inp = inp.replace('$$','')
    
    if mmode1.match(inp) != None:
        inp = inp.replace('$','')
    
    if mmode2.match(inp) != None:
        inp = inp.replace('\\[','')
        inp = inp.replace('\\]','')
    
    if mmode3.match(inp) != None:
        inp = inp.replace('\\begin{equation}','')
        inp = inp.replace('\\end{equation}','')
    
    if mmode4.match(inp) != None:
        inp = inp.replace('\\begin{eqnarray}','')
        inp = inp.replace('\\end{eqnarray}','')
        
    if mmode5.match(inp) != None:
        inp = inp.replace('\\begin{equation*}','')
        inp = inp.replace('\\end{equation*}','')
    
    if mmode6.match(inp) != None:
        inp = inp.replace('\\begin{eqnarray*}','')
        inp = inp.replace('\\end{eqnarray*}','')
    
    return inp


def tertiary_processing(inp):
    inp = inp.replace('\\nonumber', '')
    inp = inp.replace('&', ' ')
    
    inp = inp.split('\\\\')
    ret = []
    for i in inp:
        if i != '\\':
            ret.append(i.strip())
    
    return ret


def full_processing(inp):
    inp = primary_processing(inp)
    inp = [secondary_processing(i) for i in inp]
    
    processed = []
    [processed.extend(tertiary_processing(i)) for i in inp]
    processed = [i for i in processed if len(i) <= 600]
    
    return processed


def main():
    out = codecs.open('../../Data/Formulae', 'w', 'cp1252')
    metaout = codecs.open('../../Data/Meta', 'w', 'cp1252')
    
    for year in xrange(1992, 2004):
        
        print 'Processing year {0}'.format(year)
        files = os.listdir('../../Dataset/{0}'.format(year))
        
        for afile in files:
            try:
                text = open('../../Dataset/{0}/{1}'.format(year, afile), 'r').read().decode('cp1252', errors='ignore')
                for form in full_processing(text):
                    out.write(u'{0}\n'.format(form))
                    metaout.write(u'{0} {1}\n'.format(year, afile))
            except Exception as obj:
                print year, afile
                print obj
                raise

                
    out.close()
    metaout.close()
        
if __name__ == '__main__':
    main()

