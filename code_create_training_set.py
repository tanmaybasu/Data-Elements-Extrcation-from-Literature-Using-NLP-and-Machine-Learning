
import codecs
import re
import sys
import nltk
from nltk.corpus import stopwords
from nltk import tokenize

stopset = set(stopwords.words('english'))

# Tokenize any statement based on filter
def sent_to_tokens(sent):
    return filter(nltk.word_tokenize(sent))

# Longest Common Subsequence
def lcs(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
            else:
                m[x][y] = 0
    #print x_longest,longest
    #print s1[x_longest - longest: x_longest]
    #return (s1[x_longest - longest: x_longest],longest)
    return longest
    
# Final score calculation
def get_sent_score(sent,target_tokens,inp):
    sent_tokens = sent_to_tokens(sent)
    score = 0   
#   Using modified Jaccard Similarity    
    if inp=='0':
        for token in target_tokens:
            if token in sent_tokens:
                score += 1
        if score!=0:
            score = float(score)/len(target_tokens)   
    # Using LCS     
    else:
        score=lcs(sent_tokens,target_tokens)
        if score>0:
            score=score/float(len(target_tokens))     
    return (sent,score)

# Filter for the statement for tokenization
def filter(tokens):
    filtered = []
    stop_words = stopwords.words('english')
    stemmer = nltk.PorterStemmer()
    number = re.compile(r'^[0-9]*\.?$')
    for token in tokens:
        try:
            # To check punctuations
            if len(token) == 1:
                continue
            # To check for numbers
            if number.match(token):
                continue
            # To check for stopwords
            if token in stop_words:
                continue
            token = stemmer.stem(token)
            filtered.append(token)
        except UnicodeDecodeError as e:
            continue
        except UnicodeWarning as e1:
            continue
    return filtered
    
def create_training_corpora(doc,stng):
    id1=1
    id2=1
    # Addressing each file one by one
    for b in range(0,len(doc),2):
        # File name of text file to check
        name = doc[b].strip('\n')
        print name
        # Inclusion statement
        text = doc[b+1]
        try:
            # Accessing pdf text
            path = "./processed_references/" + name[:-4] + 'txt'
            filetexts = codecs.open(path,encoding='utf-8',mode='r').readlines()
            filetexts=''.join(filetexts)
            sentences = tokenize.sent_tokenize(filetexts)

            target_tokens = sent_to_tokens(text)
            scores = [get_sent_score(s,target_tokens,0) for s in sentences]    #LCS/Jaccard selection
            scores = sorted(scores, key=lambda item: item[1], reverse=True)
            
            trn_pos=stng+'positive/pv'+str(id1)+'.txt'
            trn_neg=stng+'negative/ng'+str(id2)+'.txt'
            trnp = codecs.open(trn_pos,encoding='utf-8',mode='w')
            trnn = codecs.open(trn_neg,encoding='utf-8',mode='w')

            stp=scores[0][0]   # best sentence
            #stp=scores[0][0]+'\n\n'+str(scores[0][1])+'\n\n'

            dif1=scores[0][1]-scores[1][1]
            dif2=scores[0][1]-scores[2][1]

            if dif1>=0 and dif1<=0.2:
                stp=stp+'\n\n'+scores[1][0]         # 2nd best sentence
                #stp=stp+scores[1][0]+'\n\n'+str(scores[1][1])+'\n\n'
            if dif2>=0 and dif2<=0.2:
                stp=stp+'\n\n'+scores[2][0]         # 3rd best sentence
                #stp=stp+scores[2][0]+'\n\n'+str(scores[2][1])
#            trnp.write(stp)
            # Text Refinement
            new_stp = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', stp)   # Remove special characters
            tokens = nltk.word_tokenize(new_stp)                # Remove stopwords
            tokens = [w for w in tokens if not w in stopset]
            tokens = [w.lower() for w in tokens]
            refined_tokens = ' '.join(tokens)
            for token in refined_tokens:
                trnp.write(token)
            trnp.write('\n')

            stn=''                                              # initialize stn to store the negative sentences
            for score in scores:                                # Negative examples
                if score[1]>=0 and score[1]<=0.005:
                    stn=stn+score[0]
            trnn.write(stn)
            new_stn = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', stn)   # Remove special characters
            tokens = nltk.word_tokenize(new_stn)                # Remove stopwords 
            tokens = [w for w in tokens if not w in stopset]
            tokens = [w.lower() for w in tokens]
            refined_tokens = ' '.join(tokens)
            for token in refined_tokens:
                trnn.write(token)
            trnn.write('\n')
            id1=id1+1
            id2=id2+1
        except IOError as e:
            print e
            print b
    trnp.close()
    trnn.close()

# Final Main function
def main():
#    inp1 = str(raw_input("Enter '0', if you want to create the training samples using a modified Jaccard similarity or '1' by using Longest Common Subsequence: "))
    inp = str(raw_input("Enter 'a' for inclusion statements or 'b' for interventions or 'c' for exclusion_statements: ")) 

    # Read input file
    if inp=='a':
        doc = codecs.open('inclusion_statements_with_ref.txt',encoding='utf-8',mode='r').readlines()
        stng='training_corpora/inclusion_statements/jaccard/'
    if inp=='b':
        doc = codecs.open('interventions_with_ref.txt',encoding='utf-8',mode='r').readlines()
        stng='training_corpora/interventions/jaccard/'
    if inp=='c':
        doc = codecs.open('exclusion_statements_with_ref.txt',encoding='utf-8',mode='r').readlines()
        stng='training_corpora/exclusion_statements/jaccard/'
#    else:
#        print("Wrong input")
#        sys.exit()  
    create_training_corpora(doc,stng)
 
   
if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
     
    
 