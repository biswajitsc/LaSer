import os
import re
import sys
import math
import web
import json
import urllib
import operator
from HelperFunctions import *


# render_xml = lambda message: '<message>%s</message>'%message
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
	global metadata
	global original_eqns

	latex_eqn = urllib.unquote(query).decode('utf8')

	# print "#############"
	# print "in generateRankedLists : latex_eqn is ",latex_eqn
	# print "#############"

	mathML_eqn = generateMathML(latex_eqn)

	# print "#############"
	# print "in generateRankedLists : mathML_eqn is ",mathML_eqn
	# print "#############"


	# work with both the simplified eqn as well as the original eqn

	mathML_eqns = normalizeQuery(mathML_eqn)
	print "Eqns :",len(mathML_eqns)

	simplified_mathML_eqn = simplifyMathML(mathML_eqn)	
	simplified_mathML_eqns = normalizeQuery(mathML_eqn)

	# print "#############"
	# print "in generateRankedLists : number normalized mathml is ",mathML_eqn
	# print "#############"

	# print "#############"
	# print "in generateRankedLists : unicode normalized mathml is ",mathML_eqn
	# print "#############"

	query_vectors = []
	simplified_query_vectors = []

	for eqn in mathML_eqns:
		query_vectors.append(extractWeights(eqn, idf_scores, unigrams, bigrams, trigrams))

	for eqn in simplified_mathML_eqns:
		simplified_query_vectors.append(extractWeights(eqn, idf_scores, unigrams, bigrams, trigrams))


	# Matching

	# Determine the matching docs

	# list of sets
	matched_docs_list = []
	simplified_matched_docs_list = []

	# list of dictionaries
	cosine_similarities = []
	simplified_cosine_similarities = []


	print "features in query are"
	print query_vectors
	print simplified_query_vectors

	fuck = set()

	for x in range(len(query_vectors)):
		query_vector = query_vectors[x]
		cosine_similarity = {}
		matched_docs = set()
		for feature in query_vector:
			# identify the type of feature
			if feature in unigrams:
				for doc_id, frequency in unigrams_postinglist[feature]:
					if doc_id not in cosine_similarity:
						cosine_similarity[doc_id] = 0.0
						matched_docs.add(doc_id)
					cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] #- idf_scores[feature]*query_vector[feature]fuck.add(feature)
					fuck.add(feature)

			elif feature in bigrams:
				for doc_id, frequency in bigrams_postinglist[feature]:
					if doc_id not in cosine_similarity:
						cosine_similarity[doc_id] = 0.0
						matched_docs.add(doc_id)
					cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] #- idf_scores[feature]*query_vector[feature]
					fuck.add(feature)

			elif feature in trigrams:
				for doc_id, frequency in trigrams_postinglist[feature]:
					if doc_id not in cosine_similarity:
						cosine_similarity[doc_id] = 0.0
						matched_docs.add(doc_id)
					cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] #- idf_scores[feature]*query_vector[feature]
					fuck.add(feature)
			else:
				print "This should not have happened"
		cosine_similarities.append(cosine_similarity)
		matched_docs_list.append(matched_docs)

	for x in range(len(simplified_query_vectors)):
		simplified_query_vector = simplified_query_vectors[x]
		simplified_cosine_similarity = {}
		simplified_matched_docs = set()
		for feature in simplified_query_vector:
			# identify the type of feature
			if feature in unigrams:
				for doc_id, frequency in unigrams_postinglist[feature]:
					if doc_id not in simplified_cosine_similarity:
						simplified_cosine_similarity[doc_id] = 0.0
						simplified_matched_docs.add(doc_id)
					simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] #- idf_scores[feature]*simplified_query_vector[feature]
					fuck.add(feature)

			elif feature in bigrams:
				for doc_id, frequency in bigrams_postinglist[feature]:
					if doc_id not in simplified_cosine_similarity:
						simplified_cosine_similarity[doc_id] = 0.0
						simplified_matched_docs.add(doc_id)
					simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] #- idf_scores[feature]*simplified_query_vector[feature]
					fuck.add(feature)

			elif feature in trigrams:
				for doc_id, frequency in trigrams_postinglist[feature]:
					if doc_id not in simplified_cosine_similarity:
						simplified_cosine_similarity[doc_id] = 0.0
						simplified_matched_docs.add(doc_id)
					simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] #- idf_scores[feature]*simplified_query_vector[feature]
					fuck.add(feature)
			else:
				print "This should not have happened"
		simplified_cosine_similarities.append(simplified_cosine_similarity)
		simplified_matched_docs_list.append(simplified_matched_docs)

		print 'fucked: ',fuck

	# for x in range(len(query_vectors)):
	# 	query_vector = query_vectors[x]
	# 	matched_docs = matched_docs_list[x]
	# 	for feature in query_vector:
	# 		for doc_id in matched_docs:
	# 			cosine_similarities[x][doc_id] += idf_scores[feature]*query_vector[feature]

	# for x in range(len(simplified_query_vectors)):
	# 	simplified_query_vector = simplified_query_vectors[x]
	# 	simplified_matched_docs = simplified_matched_docs_list[x]
	# 	for feature in simplified_query_vector:
	# 		for doc_id in simplified_matched_docs:
	# 			simplified_cosine_similarities[x][doc_id] += idf_scores[feature]*simplified_query_vector[feature]

	# we have the numerators
	# traverse the entire postings list to compute the denominator

	# Matching docs computed

	# determine the cosine similarity with each matched doc

	# set denoting the docs to be considered
	docs = set()
	mod_weight = {}

	for doc_ids in matched_docs_list:
		for doc_id in doc_ids:
			docs.add(doc_id)

	for doc_ids in simplified_matched_docs_list:
		for doc_id in doc_ids:
			docs.add(doc_id);

	for doc_id in docs:
		mod_weight[doc_id] = 0.0

	for feature in unigrams_postinglist:
		for doc_id, frequency in unigrams_postinglist[feature]:
			if doc_id in docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))


	for feature in bigrams_postinglist:
		for doc_id, frequency in bigrams_postinglist[feature]:
			if doc_id in docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))

	for feature in trigrams_postinglist:
		for doc_id, frequency in trigrams_postinglist[feature]:
			if doc_id in docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))

	for doc_id in docs:
		mod_weight[doc_id] = math.sqrt(mod_weight[doc_id])

	for x in range(len(cosine_similarities)):
		for doc_id in cosine_similarities[x]:
			cosine_similarities[x][doc_id] = cosine_similarities[x][doc_id]/mod_weight[doc_id]


	for x in range(len(simplified_cosine_similarities)):
		for doc_id in simplified_cosine_similarities[x]:
			simplified_cosine_similarities[x][doc_id] = simplified_cosine_similarities[x][doc_id]/mod_weight[doc_id]

	# sort the cosine similarity vales corresponding to each query variant and store in a list

	sorted_cosine_similarities_list = []
	
	for x in range(len(cosine_similarities)):
		for doc_id, score in cosine_similarities[x].items():
			sorted_cosine_similarities_list.append((doc_id,score))
	
	for x in range(len(simplified_cosine_similarities)):
		for doc_id, score in simplified_cosine_similarities[x].items():
			sorted_cosine_similarities_list.append((doc_id,score))

	sorted_cosine_similarities_list = sorted(sorted_cosine_similarities_list, key=lambda tup: tup[1], reverse=True)

	# get the best score corresponding to each doc

	ranked_list = {};
	ranked_docs = set()

	# Limit the returned results to 50

	i=0

	for doc_id, score in sorted_cosine_similarities_list:
		if doc_id not in ranked_docs:
			i += 1
			ranked_docs.add(doc_id)
			original_doc_id = metadata[int(doc_id)-1]
			original_eqn = original_eqns[int(original_doc_id.split(" ")[2]) - 1]
			original_doc_id = original_doc_id.split(" ")[1]
			tempDict = {}
			tempDict['original_doc_id'] = original_doc_id
			
			original_eqn = unicode(original_eqn, "utf-8")

			original_eqn = original_eqn.encode('ascii', 'xmlcharrefreplace')                    
			tempDict['original_eqn'] = original_eqn
			tempDict['doc_id'] = doc_id
			tempDict['score'] = score
			# ranked_list.append((doc_id,score,int(original_doc_id),original_eqn))
			ranked_list[i] = tempDict
		if i == 50:
			break

	return ranked_list

class greet:

    def GET(self, query):
        ans = generateRankedLists(query)
        latex_formulae = []
        latex_formulae.append("a = b")
        latex_formulae.append("b = c")
        archive_id = []
        archive_id.append("1")
        archive_id.append("2")
        archive_links = []
        archive_links.append('https//papers.com/1')
        archive_links.append('https//papers.com/2')
        web.header('Content-Type', 'application/json') 
        print ans
        # return str(ans).decode('utf-8')
        return json.dumps(ans,ensure_ascii=False)#, 'latex_formulae' : latex_formulae, 'archive_id' : archive_id, 'archive_links' : archive_links}

    def PUT(self,value):
        val = value
        print "PUT",val

if __name__ == "__main__":
	app.run()