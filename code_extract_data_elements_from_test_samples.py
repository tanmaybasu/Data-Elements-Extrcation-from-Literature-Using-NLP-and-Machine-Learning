
import codecs,re,sys
from nltk import tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm, grid_search
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score,confusion_matrix

stopset = set(stopwords.words('english'))
                   
# Classification using the Gold Statndard after creating it from the raw text    
def classify():
#    inp1 = raw_input("Enter No. of Positive Examples (Total Positive Sample is 69): ")
#    inp2 = raw_input("Enter No. of Negative Examples (Total Positive Sample is 69): ")
    inp = raw_input("Enter 'a' for inclusion statements or 'b' for interventions or 'c' for exclusion statements: ")
    
    inp1=67;    inp2=67
    trn_data=[];    trn_cat=[];   
    p1=0; p2=0; p3=0

    if inp=='a':
        stng='training_corpora/inclusion_statements/jaccard/'
    elif inp=='b':
        stng='training_corpora/interventions/jaccard/'
    elif inp=='c':
        stng='training_corpora/exclusion_statements/jaccard/'        
    else:
        print("Wrong input")
        exit 
       
# Preparing Positive Training Samples
    for i in range (1,int(inp1)+1):
        trn_pos=stng+'positive/pv'+str(i)+'.txt'  # File location (training using Jaccard)
        text=codecs.open(trn_pos,encoding='utf-8',mode='r').readlines()
        text=''.join(text)
        sentences = tokenize.sent_tokenize(text)
        for s in sentences:
            s = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', s)  # Remove special characters            
            trn_data.append(s)           
            trn_cat.append(0)
            p1=p1+1
  
# Preparing Negative Training Samples        
    for i in range (1,int(inp2)+1):
        trn_neg=stng+'negative/ng'+str(i)+'.txt' # File location (training using Jaccard)
        text=codecs.open(trn_neg,encoding='utf-8',mode='r').readlines()
        text=''.join(text)
        sentences = tokenize.sent_tokenize(text)
        for s in sentences:
            s = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', s)  # Remove special characters            
            trn_data.append(s)           
            trn_cat.append(1)
            p2=p2+1
      
# A pipeline of different parameters of the classifier 
    pipeline = Pipeline([
        ('vect', CountVectorizer(token_pattern=r'\b\w+\b')),
        ('tfidf', TfidfTransformer()),
        ('svr', svm.SVC(kernel='linear', class_weight='balanced')),
    ]) 
       
# Fix the values of the parameters using Grid Search and cross validation on the training samples 
    parameters = {
    'vect__min_df': (2,3),
    'vect__ngram_range': ((1, 2),(1,3)),  # unigrams or bigrams
    'tfidf__use_idf': (True, False),
    'svr__C':(0.1,10,100,1000),
    }     
    grid = grid_search.GridSearchCV(pipeline, parameters,cv=10)          
    grid.fit(trn_data, trn_cat)    
#    print("The best classifier is: ", grid.best_estimator_)
    clf= grid.best_estimator_
    
# Classification of the test samples using the fixed pipeline 
    tst_map = codecs.open('test_samples/test_file_map.txt',encoding='utf-8',mode='r').readlines()
    for b in range(0,len(tst_map),2):
        # File name of test file to check
        fl = tst_map[b].strip('\n\r') 
        print fl
        data=[];  tst_data=[];  p3=0 
        # Preparing Test Samples 
        text = codecs.open('test_samples/'+fl+'.txt',encoding='utf-8',mode='r').readlines()
        text=''.join(text)
        sentences = tokenize.sent_tokenize(text)
        for s in sentences:                               # Extracting sentences
            s = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', s)     # Remove special characters
            tst_data.append(s)  
            p3=p3+1
        data.extend(trn_data)  
        data.extend(tst_data)
        if inp=='a':
            out = codecs.open('output/inclusion_statements/svm/'+fl+'_svm.txt',encoding='utf-8',mode='w')    # Output file        
            out.write('\n Using SVM Classifier: \n\n')   
            out.write('Total No. of Sentences in the Reference: '+str(p3)+'\n\n')
            out.write('The Inclusion Statements are as Follow: \n\n')
        elif inp=='b':
            out = codecs.open('output/interventions/svm/'+fl+'_svm.txt',encoding='utf-8',mode='w')    # Output file        
            out.write('\n Using SVM Classifier: \n\n')   
            out.write('Total No. of Sentences in the Reference: '+str(p3)+'\n\n')
            out.write('The Interventions are as Follow: \n\n')            
        elif inp=='c':
            out = codecs.open('output/exclusion_statements/svm/'+fl+'_svm.txt',encoding='utf-8',mode='w')    # Output file        
            out.write('\n Using SVM Classifier: \n\n')   
            out.write('Total No. of Sentences in the Reference: '+str(p3)+'\n\n')
            out.write('The Exclusion Statements are as Follow: \n\n')            
#   Results    
        nps=0
        clf.fit(trn_data, trn_cat)
        predicted = clf.predict(tst_data)        
        for i in range(0,len(predicted)):
            if predicted[i] == 0:
                nps=nps+1
    #            print 'Relevant Sentence '+str(nps)
    #            print '\n'+data[p1+p2+i]+'\n' 
                out.write('\n'+str(nps)+")  "+tst_data[i]+'\n')               
        print("Total No. of Positive Sentences: %d" %nps)

  
if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding('utf8')
    classify()
