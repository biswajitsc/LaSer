import os
import urllib
import ConfigParser
from lxml import html
import MySQLdb as mysqldb
from urllib import urlencode, quote
from collections import OrderedDict

SOM = 1
LASER = 0
NOTOPRES = 5

# disabling proxy for localhost
os.environ['NO_PROXY'] = '127.0.0.1'

# establishing database connection
sqlconf = ConfigParser.ConfigParser()
sqlconf.read('../sql-config.ini')
db = mysqldb.connect(sqlconf.get('database', 'server'), sqlconf.get('database', 'username'), 
        sqlconf.get('database', 'password'), sqlconf.get('database', 'dbname'))
cursor = db.cursor()

def laserParser(latexQuery):
    global NOTOPRES
    head = 'http://127.0.0.1/laser-search/index.php'
    query = head + '?' + urlencode( OrderedDict( mathSnippet=latexQuery ) )
    pagesource = urllib.urlopen(query).read()
    page = html.fromstring( pagesource )
    pageTitles = page.xpath('//div[@class="search-result"]/center/a/text()')
    pageLinks = page.xpath('//div[@class="search-result"]/center/a/@href')
    pageContext = [ '$$' + x.strip() + '$$' for x in page.xpath('//div[@class="search-result"]/math/@alttext') ]
    results = zip(pageTitles, pageLinks, pageContext)
    return results[:NOTOPRES]

def searchOnMathParser(latexQuery):
    global NOTOPRES
    head = 'http://www.searchonmath.com/result'
    query = head + '?' + urlencode( OrderedDict( equation=latexQuery ) )
    pagesource = urllib.urlopen(query).read()
    page = html.fromstring( pagesource )
    pageTitles = page.xpath('//section[@class="page_content"]/article[@class="result"]/h2/a/text()')
    pageLinks = page.xpath('//section[@class="page_content"]/article[@class="result"]/h2/a/@href')
    pageContext = [ x.strip() for x in page.xpath('//section[@class="page_content"]/article[@class="result"]/div/div/text()') ]
    results = zip(pageTitles, pageLinks, pageContext)
    return results[:NOTOPRES]

def transform(value):
    value = value.replace('%\n', '')
    value = value.replace('\\', '\\\\')
    value = value.replace("'", "\\'")
    value = value.encode('utf-8')
    return value

def insertIntoTableGetId(table, value):
    value = transform(value)
    query = "SELECT id FROM " + table + " WHERE value = '" + value + "' LIMIT 1;"
    # print query
    cursor.execute(query)
    qresult = cursor.fetchall()
    if len(qresult) > 0:
        return str(qresult[0][0])
    else:
        query = "INSERT INTO " + table + " (value) VALUES('" + value + "');"
        # print query
        cursor.execute(query)
        query = "SELECT id FROM " + table + " WHERE value = '" + value + "' LIMIT 1;"
        # print query
        cursor.execute(query)
        return str(cursor.fetchall()[0][0])

def insertIntoDB(qid, queryResults, sysTyp):
    rank = 0
    for result in queryResults:
        rank += 1 
        pid = insertIntoTableGetId('papers', result[1] + ' ' + result[0]) # TODO: to ignore/consider the paper title, for now ignored
        query = "INSERT INTO modelresults (systyp, qid, rank, pid, context) VALUES(" + ",".join(["'%s'" % sysTyp, qid, str(rank), pid, "'%s'" % transform(result[2])]) + ")"
        # print query
        cursor.execute(query)

def main():
    global SOM
    global LASER
    queryFile = open('queries.txt', 'r')
    for latexQuery in queryFile:
        latexQuery = latexQuery.strip()
        qid = insertIntoTableGetId('queries', '$' + latexQuery + '$')
        somQR = searchOnMathParser(latexQuery)
        insertIntoDB(qid, somQR, str(SOM))
        laserQR = laserParser(latexQuery)
        insertIntoDB(qid, laserQR, str(LASER))
        break
    db.commit()

if __name__ == '__main__':
    main()