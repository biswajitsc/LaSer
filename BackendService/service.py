import web
import json
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
    return query

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
        generateRankedLists(query)
        latex_formulae = []
        latex_formulae.append("a = b")
        latex_formulae.append("b = c")
        archive_id = []
        archive_id.append("1")
        archive_id.append("2")
        archive_links = []
        archive_links.append('https//papers.com/1')
        archive_links.append('https//papers.com/2') 
        return {'query': query, 'latex_formulae' : latex_formulae, 'archive_id' : archive_id, 'archive_links' : archive_links}

    def PUT(self,value):
        val = value
        print "PUT",val


if __name__ == "__main__":
    app.run()
