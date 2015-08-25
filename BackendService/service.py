import os
import re
import sys
import math
import web
import json
import urllib
import operator
import mimerender
from HelperFunctions import *

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
	global unigrams
	global bigrams
	global trigrams
	global idf_scores
	global unigrams_postinglist
	global bigrams_postinglist
	global trigrams_postinglist
	global weight_matrix

	latex_eqn = urllib.unquote(query).decode('utf8')
	mathML_eqn = generateMathML(latex_eqn)

	# work with both the simplified eqn as well as the original eqn

	simplfied_mathML_eqn = simplifyMathML(mathML_eqn)
	simplfied_mathML_eqn = numberNormalize(mathML_eqn)
	simplfied_mathML_eqn = unicodeNormalize(mathML_eqn)

	mathML_eqn = numberNormalize(mathML_eqn)
	mathML_eqn = unicodeNormalize(mathML_eqn)

	query_vector = extractWeights(simplified_mathML_eqn, idf_scores, unigrams, bigrams, trigrams)
	simplified_query_vector = extractWeights(mathML_eqn, idf_scores, unigrams, bigrams, trigrams)


	# Matching

	# Determine the matching docs

	matched_docs = set()
	simplified_matched_docs = set()

	for feature in query_vector:
		# identify the type of feature
		if feature in unigrams:
			for doc_id, frequency in unigrams_postinglist[feature]:
				matched_docs.add(doc_id)

		elif feature in bigrams:
			for doc_id, frequency in bigrams_postinglist[feature]:
				matched_docs.add(doc_id)

		elif feature in trigrams:
			for doc_id, frequency in trigrams_postinglist[feature]:
				matched_docs.add(doc_id)
		
		else:
			print "This should not have happened"

	for feature in simplified_query_vector:
		# identify the type of feature
		if feature in unigrams:
			for doc_id, frequency in unigrams_postinglist[feature]:
				simplified_matched_docs.add(doc_id)

		elif feature in bigrams:
			for doc_id, frequency in bigrams_postinglist[feature]:
				simplified_matched_docs.add(doc_id)

		elif feature in trigrams:
			for doc_id, frequency in trigrams_postinglist[feature]:
				simplified_matched_docs.add(doc_id)
		
		else:
			print "This should not have happened"


	# Matching docs computed

	# determine the cosine similarity with each matched doc

	cosine_similarity = {}
	simplified_cosine_similarity = {}

	for doc_id in matched_docs:
		dot_product = 0.0
		for feature in query_vector:
			dot_product += query_vector[feature]*weight_matrix[doc_id][feature]
		cosine_similarity[doc_id] = dot_product;

	for doc_id in simplified_matched_docs:
		dot_product = 0.0
		for feature in simplified_query_vector:
			dot_product += simplified_query_vector[feature]*weight_matrix[doc_id][feature]
		simplified_cosine_similarity[doc_id] = dot_product;

	sorted_cosine_similarity = sorted(cosine_similarity.items(), key=operator.itemgetter(1))
	sorted_simplified_cosine_similarity = sorted(simplified_cosine_similarity.items(), key=operator.itemgetter(1))

	# cosine similariy determined

	# generate the json
	
	ranked_list = [];

	iter_1 = 0
	iter_2 = 0

	while(iter_1 != len(sorted_cosine_similarity) and iter_2 != len(sorted_simplified_cosine_similarity)):
		if iter_1 < len(sorted_cosine_similarity) and iter_2 < len(sorted_simplified_cosine_similarity):
			if sorted_cosine_similarity[iter_1][1] < sorted_simplified_cosine_similarity[iter_2][1]:
				ranked_list.append((sorted_simplified_cosine_similarity[iter_2][0],sorted_simplified_cosine_similarity[iter_2][1]))
				iter_2 += 1
			else:
				ranked_list.append((sorted_cosine_similarity[iter_1][0],sorted_cosine_similarity[iter_1][1]))
				iter_1 += 1
		elif iter_1 != len(sorted_cosine_similarity):
			ranked_list.append((sorted_cosine_similarity[iter_1][0],sorted_cosine_similarity[iter_1][1]))
			iter_1 += 1
		else:
			ranked_list.append((sorted_simplified_cosine_similarity[iter_2][0],sorted_simplified_cosine_similarity[iter_2][1]))
			iter_2 += 1

	ranked_result = JSONEncoder().encode(ranked_list)

	return ranked_result

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
        print "query is", query
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

unigrams = set()
bigrams = set()
trigrams = set()
idf_scores = {}
unigrams_postinglist = {}
bigrams_postinglist = {}
trigrams_postinglist = {}
weight_matrix = []

if __name__ == "__main__":
	(unigrams, bigrams, trigrams, idf_scores, unigrams_postinglist, bigrams_postinglist, trigrams_postinglist, weight_matrix) = generateIndex(sys.argv[2])
	app.run()
