import os
import sys


def main():
    stars = "*********************************************"
    infile = sys.argv[1]
    outfile = sys.argv[2]
    print 'Reading from', infile
    print 'Writing to', outfile

    errfile = open(infile, 'r')
    writefile = open(outfile, 'w')

    errlist = errfile.read().split(stars)
    size = len(errlist)
    i = 0
    while True:
        if 2 * i + 1 >= size:
            break
        temp = errlist[2 * i + 1].split('\n')
        temp = temp[1]
        writefile.write(temp + '\n')
        i += 1

    errfile.close()
    writefile.close()

if __name__ == '__main__':
    main()
