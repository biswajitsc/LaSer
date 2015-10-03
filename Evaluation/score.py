import MySQLdb as mysqldb
import ConfigParser
import math

# number of search systems
S = 2
# number of search results per query
K = 3

# establishing database connection
sqlconf = ConfigParser.ConfigParser()
sqlconf.read('sql-config.ini')
db = mysqldb.connect(sqlconf.get('database', 'server'), sqlconf.get('database', 'username'), 
		sqlconf.get('database', 'password'), sqlconf.get('database', 'dbname'))
cursor = db.cursor()

def precision(systyp, q, users):
	global K
	# Compute precision@[1...K] for (query, user) pair
	PatK = {}
	avgrel = [0.0] * K
	for u in users:
		query = "SELECT oldrank, relevant FROM evalresults WHERE uid = " + str(u) + " AND qid = " + str(q) + \
			" AND systyp = '" + str(systyp) + "' ORDER BY oldrank;"
		cursor.execute(query)
		uqresults = cursor.fetchall()
		if len(uqresults) < K:
			print '#results on query(' + str(q) + ') and user(' + str(u) + ') is less than K(' + K + ')'
			continue
		else:
			PatK[u] = []
			for k in range(K):
				reluk = float(uqresults[k][1]) / 2.0 # divide by 2.0 to bring relevance in [0, 1]
				avgrel[k] += reluk
				if k > 0:
					PatK[u].append( (PatK[u][k - 1] * k + reluk)/(k+1) )
				else:
					PatK[u].append( reluk/(k+1) )
	avgPatK = [0.0] * K
	for u in users:
		for k in range(K):
			avgPatK[k] += PatK[u][k]
	for k in range(K):
		avgPatK[k] /= len(users)

	return avgPatK

def dcg(systyp, q, users):
	global K
	# Compute avg DCG, avg nDCG for (query, user) pair and also DCG, nDCG for (query, averaged-user) pair
	DCG = {}
	optDCG = {}
	avgmr = [[0.0, 0.0]] * K
	for u in users:
		query = "SELECT oldrank, newrank, relevant FROM evalresults WHERE uid = " + str(u) + " AND qid = " + str(q) + \
			" AND systyp = '" + str(systyp) + "' ORDER BY oldrank;"
		cursor.execute(query)
		uqresults = cursor.fetchall()
		if len(uqresults) < K:
			print '#results on query(' + str(q) + ') and user(' + str(u) + ') is less than K(' + str(K) + ')'
			continue
		else:
			DCG[u] = 0.0
			mxr = []
			for k in range(K):
				multiplier = (len(uqresults) - float(uqresults[k][1]) + 1)
				relevance = float(uqresults[k][2]) / 2.0 # divide by 2.0 to bring relevance in [0, 1]
				if k > 0:
					DCG[u] += multiplier * relevance / math.log(float(k + 1), 2)
				else:
					DCG[u] += multiplier * relevance
				mxr.append(multiplier * relevance)
				avgmr[k][0] += multiplier
				avgmr[k][1] += relevance
			optDCG[u] = 0.0
			sorted(mxr, reverse=True)
			for k in range(K):
				if k > 0:
					optDCG[u] += mxr[k] / math.log(float(k + 1), 2)
				else:
					optDCG[u] += mxr[k]
	# Compute DCG for (query, user) pair
	DCG_1 = 0.0
	for u in users:
		DCG_1 += DCG[u]
	DCG_1 /= len(users)
	# Compute nDCG for (query, user) pair
	nDCG_1 = 0.0
	for u in users:
		nDCG_1 += (DCG[u] / optDCG[u])
	nDCG_1 /= len(users)
	# Compute DCG for (query, averaged-user)
	DCG_2 = 0.0
	for k in range(K):
		avgmr[k][0] /= len(users)
		avgmr[k][1] /= len(users)
		if k > 0:
			DCG_2 += avgmr[k][0] * avgmr[k][1] / math.log(float(k + 1), 2)
		else:
			DCG_2 += avgmr[k][0] * avgmr[k][1]
	# Compute nDCG for (query, averaged-user)
	optDCG_2 = 0.0
	avgmr = sorted(avgmr, key=lambda mr: mr[0] * mr[1], reverse=True)
	for k in range(K):
		if k > 0:
			optDCG_2 += ( avgmr[k][0] * avgmr[k][1] / math.log(float(k + 1), 2) )
		else:
			optDCG_2 += ( avgmr[k][0] * avgmr[k][1] )
	nDCG_2 = DCG_2 / optDCG_2
	return ((DCG_1, DCG_2), (nDCG_1, nDCG_2))

def main():
	global S
	global K
	for systyp in range(S):
		PRECatK = [0.0] * K
		DCG = [0.0, 0.0]
		nDCG = [0.0, 0.0]
		print 'System', systyp, 'Results'
		P = {}
		D = {}
		nD = {}
		query = "SELECT DISTINCT qid, uid FROM evalresults WHERE systyp=\'" + str(systyp) + "\' ORDER BY qid, uid;"
		cursor.execute(query)
		qulist = cursor.fetchall()
		qudict = {}
		for qu in qulist:
			q = qu[0]
			u = qu[1]
			if q in qudict:
				qudict[q].append(u)
			else:
				qudict[q] = [u]
		for q in qudict:
			(D[q], nD[q]) = dcg(systyp, q, qudict[q])
			P[q] = precision(systyp, q, qudict[q])
			for k in range(K):
				PRECatK[k] += P[q][k]
			for m in range(2):
				DCG[m] += D[q][m]
				nDCG[m] += nD[q][m]

		# Printing Results
		PatK = [ patk / len(qudict.keys()) for patk in PRECatK ]
		print '\t\tPrecision@[1...K] :', PatK
		desc = [ '(average over users)', '(averaged user)' ]
		for m in range(2):
			print '\tMethod', str(m+1), ':', desc[m]
			print '\t\tDCG :', DCG[m] / len(qudict.keys())
			print '\t\tnDCG :', nDCG[m] / len(qudict.keys())
		print '\n',

if __name__ == '__main__':
	main()