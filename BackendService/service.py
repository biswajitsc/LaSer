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

	latex_eqn = urllib.unquote(query).decode('utf8')

	# print "#############"
	# print "in generateRankedLists : latex_eqn is ",latex_eqn
	# print "#############"

	mathML_eqn = generateMathML(latex_eqn)

	# print "#############"
	# print "in generateRankedLists : mathML_eqn is ",mathML_eqn
	# print "#############"


	# work with both the simplified eqn as well as the original eqn

	simplified_mathML_eqn = simplifyMathML(mathML_eqn)
	simplified_mathML_eqn = numberNormalize(mathML_eqn)
	simplified_mathML_eqn = unicodeNormalize(mathML_eqn)

	mathML_eqn = numberNormalize(mathML_eqn)

	# print "#############"
	# print "in generateRankedLists : number normalized mathml is ",mathML_eqn
	# print "#############"


	mathML_eqn = unicodeNormalize(mathML_eqn)

	# print "#############"
	# print "in generateRankedLists : unicode normalized mathml is ",mathML_eqn
	# print "#############"



	query_vector = extractWeights(mathML_eqn, idf_scores, unigrams, bigrams, trigrams)
	simplified_query_vector = extractWeights(simplified_mathML_eqn, idf_scores, unigrams, bigrams, trigrams)


	# Matching

	# Determine the matching docs

	matched_docs = set()
	simplified_matched_docs = set()

	cosine_similarity = {}
	simplified_cosine_similarity = {}


	print "features in query are"
	for feature in query_vector:
		print feature


	for feature in query_vector:
		# identify the type of feature
		if feature in unigrams:
			for doc_id, frequency in unigrams_postinglist[feature]:
				if doc_id not in cosine_similarity:
					cosine_similarity[doc_id] = 0.0
					matched_docs.add(doc_id)
				cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] - idf_scores[feature]*query_vector[feature]

		elif feature in bigrams:
			for doc_id, frequency in bigrams_postinglist[feature]:
				if doc_id not in cosine_similarity:
					cosine_similarity[doc_id] = 0.0
					matched_docs.add(doc_id)
				cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] - idf_scores[feature]*query_vector[feature]

		elif feature in trigrams:
			for doc_id, frequency in trigrams_postinglist[feature]:
				if doc_id not in cosine_similarity:
					cosine_similarity[doc_id] = 0.0
					matched_docs.add(doc_id)
				cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] - idf_scores[feature]*query_vector[feature]
		
		else:
			print "This should not have happened"

	for feature in simplified_query_vector:
		# identify the type of feature
		if feature in unigrams:
			for doc_id, frequency in unigrams_postinglist[feature]:
				if doc_id not in simplified_cosine_similarity:
					simplified_cosine_similarity[doc_id] = 0.0
					simplified_matched_docs.add(doc_id)
				simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] - idf_scores[feature]*simplifiedquery_vector[feature]

		elif feature in bigrams:
			for doc_id, frequency in bigrams_postinglist[feature]:
				if doc_id not in simplified_cosine_similarity:
					simplified_cosine_similarity[doc_id] = 0.0
					simplified_matched_docs.add(doc_id)
				simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] - idf_scores[feature]*simplified_query_vector[feature]

		elif feature in trigrams:
			for doc_id, frequency in trigrams_postinglist[feature]:
				if doc_id not in simplified_cosine_similarity:
					simplified_cosine_similarity[doc_id] = 0.0
					simplified_matched_docs.add(doc_id)
				simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] - idf_scores[feature]*simplified_query_vector[feature]
		
		else:
			print "This should not have happened"


	for feature in query_vector:
		for doc_id in matched_docs:
			cosine_similarity[doc_id] += idf_scores[feature]*query_vector[feature];
		for doc_id in simplified_matched_docs:
			simplified_cosine_similarity[doc_id] += idf_scores[feature]*simplified_query_vector[feature];

	# we have the numerators
	# traverse the entire postings list to compute the denominator

	# Matching docs computed

	# determine the cosine similarity with each matched doc

	mod_weight = {}
	simplified_mod_weight = {}

	for doc_id in matched_docs:
		mod_weight[doc_id] = 0.0

	for doc_id in simplified_matched_docs:
		simplified_mod_weight[doc_id] = 0.0

	for feature in unigrams_postinglist:
		for doc_id, frequency in unigrams_postinglist[feature]:
			if doc_id in matched_docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))
			if doc_id in simplified_matched_docs:
				simplified_mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))


	for feature in bigrams_postinglist:
		for doc_id, frequency in unigrams_postinglist[feature]:
			if doc_id in matched_docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))
			if doc_id in simplified_matched_docs:
				simplified_mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))

	for feature in trigrams_postinglist:
		for doc_id, frequency in unigrams_postinglist[feature]:
			if doc_id in matched_docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))
			if doc_id in simplified_matched_docs:
				simplified_mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))

	for doc_id in matched_docs:
		mod_weight[doc_id] = math.sqrt(mod_weight[doc_id])

	for doc_id in simplified_matched_docs:
		simplified_mod_weight[doc_id] = math.sqrt(simplified_mod_weight[doc_id])

	for doc_id in cosine_similarity:
		cosine_similarity[doc_id] = cosine_similarity[doc_id]/mod_weight[doc_id]

	for doc_id in simplified_cosine_similarity:
		simplified_cosine_similarity[doc_id] = simplified_cosine_similarity[doc_id]/simplified_mod_weight[doc_id]



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

	ranked_result = json.JSONEncoder().encode(ranked_list)

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

if __name__ == "__main__":
	app.run()