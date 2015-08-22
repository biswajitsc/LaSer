import os
import re
import sys
import web
import json
import urllib
import mimerender

mimerender = mimerender.WebPyMimeRender()

# render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
# render_html = lambda message: '<html><body>%s</body></html>'%message
# render_txt = lambda message: message

urls = (
    '/(.*)', 'greet'
)
app = web.application(urls, globals())
val = 0

def generateRankedLists(query) :
    query = urllib.unquote(query).decode('utf8')
    mathml_representation = generateMathml(query)
    return mathml_representation

def generateMathml(eqn) :
    cleanEqn = eqn.strip('\n').strip()
    cleanEqn = re.sub('\\\\','\\\\\\\\',cleanEqn)
    cleanEqn = re.sub('\)','\\\\)',cleanEqn)
    cleanEqn = re.sub('\(','\\\\(',cleanEqn)
    # print cleanEqn
    oscommand = 'latexmlmath --pmml=- ' + cleanEqn + ' > temp.txt'
    # print oscommand
    os.system(oscommand)
    return open('temp.txt','r').read()

class greet:

    @mimerender(
        default = 'json',
        json = render_json
        # html = render_html,
        # xml  = render_xml,
        # json = render_json,
        # txt  = render_txt
    )
    def GET(self, query):
        ans = generateRankedLists(query)
        print "ans is", ans
        latex_formulae = []
        latex_formulae.append("a = b")
        latex_formulae.append("b = c")
        archive_id = []
        archive_id.append("1")
        archive_id.append("2")
        archive_links = []
        archive_links.append('https//papers.com/1')
        archive_links.append('https//papers.com/2') 
        return {'query': ans}#, 'latex_formulae' : latex_formulae, 'archive_id' : archive_id, 'archive_links' : archive_links}

    def PUT(self,value):
        val = value
        print "PUT",val


if __name__ == "__main__":
    app.run()