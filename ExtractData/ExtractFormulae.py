import os
import re
import sys
import codecs
import resource
import signal
import time

mmode0 = re.compile(r'\$\$.+?\$\$', flags=re.DOTALL | re.UNICODE)
mmode1 = re.compile(r'\$.+?\$', flags=re.DOTALL | re.UNICODE)
mmode2 = re.compile(r'\\\[.+?\\\]', flags=re.DOTALL | re.UNICODE)
mmode3 = re.compile(
    r'\\begin{equation}.+?\\end{equation}',
    flags=re.DOTALL | re.UNICODE)
mmode4 = re.compile(
    r'\\begin{eqnarray}.+?\\end{eqnarray}',
    flags=re.DOTALL | re.UNICODE)
mmode5 = re.compile(
    r'\\begin{equation\*}.+?\\end{equation\*}',
    flags=re.DOTALL | re.UNICODE)
mmode6 = re.compile(
    r'\\begin{eqnarray\*}.+?\\end{eqnarray\*}',
    flags=re.DOTALL | re.UNICODE)

clean0 = re.compile(r'.*\\newcommand.*', flags=re.IGNORECASE)
clean1 = re.compile(r'%.*')
clean2 = re.compile(r'.*\\def.*', flags=re.IGNORECASE)
clean3 = re.compile(r'\\begin{document}', flags=re.IGNORECASE)
clean4 = re.compile(r'maketitle', flags=re.IGNORECASE)
clean5 = re.compile(r'\\end{titlepage}', flags=re.IGNORECASE)
clean6 = re.compile(r'.*\\renewcommand.*', flags=re.IGNORECASE)


class Timeout():

    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))


def getdefsplits(macstr):
    macstr = macstr.strip()
    macstr = macstr[4:].strip()
    first = -1
    for i in xrange(len(macstr)):
        if macstr[i] == '{':
            first = i
            break
        if macstr[i] == '[':
            return (macstr[0:i].strip(), ' ')
        if macstr[i] == '#':
            return (macstr[0:i].strip(), ' ')
    macro = macstr[0:first].strip()
    replacement = macstr[first:].strip()[1:-1]
    return (macro, replacement)


def getcommsplits(macstr, maclen):
    macstr = macstr.strip()
    macstr = macstr[maclen:].strip()
    first = -1
    for i in xrange(len(macstr)):
        if macstr[i] == '}':
            first = i
            break
    macro = macstr[1:first].strip()
    if macstr[first + 1:].strip()[0] == '[':
        return (macro, ' ')
    replacement = macstr[first + 1:].strip()[1:-1]
    return (macro, replacement)


def primary_processing(inp):

    inp = clean0.sub('', inp)
    inp = clean1.sub('', inp)
    inp = clean2.sub('', inp)

    m = clean3.search(inp)
    if m is not None:
        inp = inp[m.end():]

    m = clean4.search(inp)
    if m is not None:
        inp = inp[m.end():]

    m = clean5.search(inp)
    if m is not None:
        inp = inp[m.end():]

    # print inp

    s0 = mmode0.findall(inp)
    inp = mmode0.sub('', inp)

    # s1 = mmode1.findall(inp)
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
    # [ret.append(i) for i in s1]
    [ret.append(i) for i in s2]
    [ret.append(i) for i in s3]
    [ret.append(i) for i in s4]
    [ret.append(i) for i in s5]
    [ret.append(i) for i in s6]

    return ret


def secondary_processing(inp):
    inp = inp.replace('\n', ' ')

    if mmode0.match(inp) != None:
        inp = inp.replace('$$', '')

    if mmode1.match(inp) != None:
        inp = inp.replace('$', '')

    if mmode2.match(inp) != None:
        inp = inp.replace('\\[', '')
        inp = inp.replace('\\]', '')

    if mmode3.match(inp) != None:
        inp = inp.replace('\\begin{equation}', '')
        inp = inp.replace('\\end{equation}', '')

    if mmode4.match(inp) != None:
        inp = inp.replace('\\begin{eqnarray}', '')
        inp = inp.replace('\\end{eqnarray}', '')

    if mmode5.match(inp) != None:
        inp = inp.replace('\\begin{equation*}', '')
        inp = inp.replace('\\end{equation*}', '')

    if mmode6.match(inp) != None:
        inp = inp.replace('\\begin{eqnarray*}', '')
        inp = inp.replace('\\end{eqnarray*}', '')

    return inp


def tertiary_processing(inp):
    inp = inp.replace('\\nonumber', '')
    inp = inp.replace('&', ' ')

    # inp = re.sub(r'\\\(.*?\)', '', inp)
    # inp = inp.replace('"', '')

    inp = inp.split('\\\\')
    ret = []
    for i in inp:
        if i != '\\':
            ret.append(i.strip())

    ret = [i for i in ret if len(i) <= 500 and len(i) > 2]
    # ret = [i for i in ret if not i.startswith('^')]

    return ret


def full_processing(inp):
    maxlen = 5000000
    if len(inp) > maxlen:
        print 'Skipping ... Length = ', len(inp)
        return []

    newcoms = clean0.findall(inp)
    defs = clean2.findall(inp)
    renewcoms = clean6.findall(inp)

    print newcoms, defs, renewcoms
    pairs = []

    for mac in defs:
        try:
            p = getdefsplits(mac)
            pairs.append(p)
        except Exception as e:
            print e

    for mac in newcoms:
        try:
            p = getcommsplits(mac, len('\\newcommand'))
            pairs.append(p)
        except Exception as e:
            print e

    for mac in renewcoms:
        try:
            p = getcommsplits(mac, len('\\renewcommand'))
            pairs.append(p)
        except Exception as e:
            print e

    pairs.sort(key=lambda x: -len(x[0]))

    for m, r in pairs:
        inp = inp.replace(m, r)
        if len(inp) > maxlen:
            print 'Skipping ... Length = ', len(inp)
            return []

    # if inp.find('\\begin{document}') == -1:
    #     return []
    # print "Done"
    inp = primary_processing(inp)
    inp = [secondary_processing(i) for i in inp]

    processed = []
    [processed.extend(tertiary_processing(i)) for i in inp]

    return processed


def main():

    # limit_memory(5000000000)
    # x = full_processing(
    #     open('../../Dataset/2003/0301050', 'r')
    #     .read().decode('cp1252', errors='ignore'))
    # for i in x:
    #     print i

    # sys.exit()

    out = codecs.open('../../Data/Formulae', 'w', 'cp1252')
    metaout = codecs.open('../../Data/Meta', 'w', 'cp1252')

    cnt = 0
    skipped = 0

    for year in reversed(xrange(1992, 2004)):

        print 'Processing year {0}'.format(year)
        files = os.listdir('../../Dataset/{0}'.format(year))

        for afile in files:
            cnt += 1
            print 'Doing', afile, 'Done ', cnt, 'Skipped ', skipped

            try:
                text = open(
                    '../../Dataset/{0}/{1}'.format(year, afile), 'r'
                ).read().decode('cp1252', errors='ignore')

                with Timeout(60):
                    allform = full_processing(text)

                if len(allform) == 0:
                    skipped += 1
                    print "Skipped ", afile

                for form in allform:
                    out.write(u'{0}\n'.format(form))
                    metaout.write(u'{0} {1}\n'.format(year, afile))

            except Exception as obj:
                skipped += 1
                print year, afile
                print obj

    out.close()
    metaout.close()

if __name__ == '__main__':
    main()
