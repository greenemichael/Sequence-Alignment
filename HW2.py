'''#################################
Michael Greene 4766783 gree1886
Needleman-Wunsch implementation
#################################'''

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#important configurable variables
_cmismatch = -3
_cmatch = 1
_cgap = -2

#reflen and qlen are integers
def init_scoring_matrix(reflen, qlen):
    #initalize with zeros
    #horizontal: reference; vertical: query
    scoreMat = np.zeros((qlen+1, reflen+1)) #extra row & col for initial gaps
    
    #add initial gap penalties
    for i in range(1, reflen+1):
        scoreMat[0][i] = scoreMat[0][i-1] + _cgap #always add the cost
    for i in range(1, qlen+1):
        scoreMat[i][0] = scoreMat[i-1][0] + _cgap
        
    return scoreMat

#assume ref and query are strings
def needleman_wunsch(ref, query):
    reflen = len(ref)
    qlen = len(query)
    
    #initialize the scoring matrix
    scoreMat = init_scoring_matrix(reflen, qlen)
    
    #horizontal: reference; vertical: query- important for interpreting penalties
    #consume each base in the reference and query strings, building score matrix
    for i in range(1, qlen+1):
        for j in range(1, reflen+1):
            #enumerate options then pick the one maximizing score
            
            #insert a gap into the reference string, consume a query base
            cconsumeQuery = scoreMat[i-1][j] + _cgap
            
            #insert a gap into the query string, consume a reference base
            cconsumeRef = scoreMat[i][j-1] + _cgap
            
            #consume a base from both strings, check for match/mismatch
            cconsumeBoth = scoreMat[i-1][j-1] + \
            (_cmatch if (query[i-1] == ref[j-1]) else _cmismatch)
            #use i-1 and j-1 because matrix traversal started at i, j = 1 but query and ref start at index 0
            
            #update scoreMat with the optimal option
            scoreMat[i][j] = max(cconsumeQuery, cconsumeRef, cconsumeBoth)
            
    #do this before modifying qlen and reflen in the following lines
    alignmentScore = scoreMat[qlen][reflen]
    
    #start from the bottom right of the matrix, walk to the top left
    #maximize the path's score and build solution sequences at the same time
    reverseRef = ""
    reverseQuery = ""
    
    #qlen is the index of the last base in the query string, same for reflen
    while qlen > 0 or reflen > 0: #dont use index >= 0 because index = 0 is the initial gap row/col
        
        if qlen <= 0: #query is completely consumed, add a gap to query and consume reference
            reverseQuery += "_"
            reverseRef += ref[reflen-1]
            reflen -= 1
            
        elif reflen <= 0: #reference is completely consumed, add a gap to reference and consume query
            reverseRef += "_"
            reverseQuery += query[qlen-1]
            qlen -= 1
            
        else:
            #enumerate options, pick the option with maximum score
            
            #insert a gap into the reference string, consume a query base
            sconsumeQuery = scoreMat[qlen-1][reflen]

            #insert a gap into the query string, consume a reference base
            sconsumeRef = scoreMat[qlen][reflen-1]
            
            #consume a base from both strings, check for match/mismatch
            sconsumeBoth = scoreMat[qlen-1][reflen-1]
            
            maxscore = max(sconsumeQuery, sconsumeRef, sconsumeBoth)
            
            if maxscore == sconsumeBoth: #consume a base from both strings
                reverseRef += ref[reflen-1]
                reverseQuery += query[qlen-1]
                reflen -= 1
                qlen -= 1
                
            elif maxscore == sconsumeRef: #tie-breaker: if max == refscore == queryscore then consume reference first
                reverseRef += ref[reflen-1]
                reverseQuery += "_"
                reflen -= 1
                
            else: #consume a base from query string
                reverseQuery += query[qlen-1]
                reverseRef += "_"
                qlen -= 1
                
    return([reverseRef[::-1], reverseQuery[::-1], alignmentScore])

#assume match is a 2d array size n*4
def anchored_needleman_wunsch(ref, query, match=None):
	print("beginning initial alignment")

	#if not anchored, do regular needleman-wunsch
	if not match: return(needleman_wunsch(ref, query))

	roffset = 0 #keeps track of the offset in the human sequence
	qoffset = 0 #how much of the fly sequence has been processed

	#return values- built as program execution proceeds
	refstr = ""
	qstr = ""
	alignscore = 0
	    
	#for each anchor: align the area, and the area between the last anchor and the current one
	#dont let aligned mismatch areas be replicated and aligned twice (use a string offset)
	for i in range(len(match)):        
	    #the first two columns of match are for the start and end positions of the human (reference) sequence
	    #last two are for the start and end position of the fly (query) sequence
	    rlow = int(match[i][0])
	    rhigh = int(match[i][1])
	    qlow = int(match[i][2])
	    qhigh = int(match[i][3])
	        
	    before = needleman_wunsch(ref[roffset:rlow], query[qoffset:qlow]) #mismatch region between previous and current anchor
	    anchor = needleman_wunsch(ref[rlow:rhigh], query[qlow:qhigh]) 
	    #must align anchors because they arent guaranteed to be 100% match (no harm if they were 100% match)
	        
	    refstr += (before[0] + anchor[0]) #order is important, this is not a symmetric operation!
	    qstr += (before[1] + anchor[1])
	    alignscore += (before[2] + anchor[2]) #this one is symmetric
	        
	    #each iteration aligns the anchor and the region preceding it (succeeding the previous anchor)
	    #this means the region following the last anchor isnt implicitly aligned!
	    #check for last anchor
	    if i == len(match)-1:
	        #explicitly align the region following the last anchor
	        after = needleman_wunsch(ref[rhigh:], query[qhigh:])
	        refstr += after[0]
	        qstr += after[1]
	        alignscore += after[2]
	            
	    #increment the reference and query offset- otherwise the same region will be aligned several times
	    roffset = rhigh #high is the index of the transition from anchor into the next mismatch region
	    qoffset = qhigh
	       
	return [refstr, qstr, alignscore]	

def permute_and_graph(ref, query):
	print("beginning permutations")

	scores = [needleman_wunsch(ref, query)[2]] #add the unpermuted score first

	i = 0
	while i<10000:
	    i += 1 #because I would've forgotten if this were last
	    refperm = "".join(np.random.permutation(list(ref))) #permutation operates on the list of chars represented by ref
	    queryperm = "".join(np.random.permutation(list(query))) #"".join() joins into a string each char in the array returned by permutation

	    #return from needleman-wunsch is [refstring, querystring, score]
	    #dont use anchored needleman-wunsch because the matches are meaningless after permuting sequences
	    scores.append(needleman_wunsch(refperm, queryperm)[2])

	figure = plt.figure()
	plt.hist(scores, bins=100)
	plt.axvline(scores[0], linestyle="dashed", label="unpermuted score") #add a vertical line to show the unpermuted score
	plt.title("frequency of alignment scores for random permutations of human and fruit fly hox genes")
	plt.xlabel("alignment score")
	plt.ylabel("frequency")
	plt.legend()
	plt.show()
	figure.savefig("AlignmentScoreHistogram.pdf")


if __name__ == '__main__':
	#invoke this program as python HW2.py <reference> <query> [<match>] [<perform permutations>]
	#sys.argv[0] = script name
	reffile = sys.argv[1]
	queryfile = sys.argv[2]
	matchfile = None if len(sys.argv) <= 3 else sys.argv[3]
		
	try: refstr = pd.read_csv(reffile)
	except: print("failed to open reference file")
	refstr = refstr[refstr.columns[0]] #specific to how pandas reads a csv into a data frame

	try: querystr = pd.read_csv(queryfile)
	except: print("failed to open query file")
	querystr = querystr[querystr.columns[0]]

	try: 
		match_unprocessed = open(matchfile, "r")
		match_tmp = match_unprocessed.read().trim().split("\n") #must be open before read (greedy exec)
		matchv = list(map(lambda group:
			group.split("\t"), match_tmp))
	except: #exception caught when match file is not supplied
		matchv = None

	alignment = anchored_needleman_wunsch(refstr, querystr, matchv)

	output = open("out.txt", "w+")
	output.write("Refrence: \n\t" + str(alignment[0]))
	output.write("\n\nQuery: \n\t" + str(alignment[1]))
	output.write("\nAlignment score: " + str(alignment[2]))
	output.close() #if performing permutations times out (it takes a while to perform) then output from NW will still be output to text

	if input("Permute and graph? type Y/N: ") == "Y": permute_and_graph(refstr, querystr)

	print("Execution finished successfully")

