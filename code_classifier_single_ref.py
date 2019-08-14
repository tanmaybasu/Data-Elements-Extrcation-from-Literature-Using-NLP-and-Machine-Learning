import os
import codecs
import re
import sys
import math
import nltk
import sklearn
from collections import OrderedDict
from nltk.collocations import *
from nltk import tokenize
from nltk.corpus import stopwords
from pprint import pprint
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation, grid_search
from sklearn.metrics import f1_score
from sklearn import svm

stopset = set(stopwords.words('english'))

# Classification using the Gold Statndard after creating it from the raw text    
def classify():
#    inp1 = raw_input("Enter No. of Positive Examples (Total Positive Sample is 69): ")
#    inp2 = raw_input("Enter No. of Negative Examples (Total Positive Sample is 69): ")

    inp1=69;    inp2=69;
    data=[];    trn_cat=[];   
    p1=0; p2=0; p3=0
    
# Preparing Positive Training Samples
    for i in range (1,int(inp1)+1):
        trn_pos='training_cdsr/jaccard/positive/pv'+str(i)+'.txt'          # File location
        text=codecs.open(trn_pos,encoding='utf-8',mode='r').readlines()
        text=''.join(text)
        sentences = tokenize.sent_tokenize(text)
        for s in sentences:
            s = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', s)  # Remove special characters
            data.append(s)           
            trn_cat.append(0)
            p1=p1+1
   
# Preparing Negative Training Samples        
    for i in range (1,int(inp2)+1):
        trn_neg='training_cdsr/jaccard/negative/ng'+str(i)+'.txt'          # File location
        text=codecs.open(trn_neg,encoding='utf-8',mode='r').readlines()
        text=''.join(text)
        sentences = tokenize.sent_tokenize(text)
        for s in sentences:
            s = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', s)  # Remove special characters
            data.append(s)           
            trn_cat.append(1)
            p2=p2+1
    
#   Preparing Test Samples   
    fl='tst9'                                   # name of the test file
    text = codecs.open('test_cdsr/'+fl+'.txt',encoding='utf-8',mode='r').readlines()
    text=''.join(text)
#    sentences = re.split('[.?!]', text)
    sentences = tokenize.sent_tokenize(text)
    for sent in sentences:                               # Extracting sentences
        sent = re.sub('[^a-zA-Z0-9.?:!$\n]', ' ', sent)  # Remove special characters
        data.append(sent)  
#       tst_cat.append(0)
        p3=p3+1
#    print ("Number of Sentences in the Test Set %d" %p3)
             
#   trigram model of raw text
    count_trigram = CountVectorizer(ngram_range=(1,3),token_pattern=r'\b\w+\b', min_df=2)
#    count_bigram = CountVectorizer()
    trigram = count_trigram.fit_transform(data)
    train_trigram = trigram[0:p1+p2]
    tst_trigram = trigram[(p1+p2):(p1+p2+p3)]          # Entire test set

#   Classification of the Test Samples using SVM
    nps=0
    val=1.0; frac=1.0;        
#    cval=fix_cval(train_trigram,trn_cat,val,frac)   # C value    
    parameters = [{'kernel':('linear','rbf'), 'C':[0.1,10,100,1000]}]
    svr = svm.SVC(kernel='linear', class_weight='balanced')
    clf = grid_search.GridSearchCV(svr, parameters,cv=10)
#    clf = svm.SVC(kernel='linear', C=cval, class_weight='balanced') 
#    clf = svm.NuSVC(kernel='linear', nu=0.1, class_weight='balanced')    
#    clf = svm.LinearSVC(C=CVAL,class_weight='balanced',loss='l2', penalty='l1', dual=False)
#    clf = svm.LinearSVC(C=1,class_weight='balanced', dual=False)    
   
    clf.fit(train_trigram, trn_cat)
    predicted = clf.predict(tst_trigram) 
    out = codecs.open('output_cdsr/tst_svm.txt',encoding='utf-8',mode='w')       # Output file        
    out.write('\n Using SVM Classifier: \n\n')
    for i in range(0,len(predicted)):
        if predicted[i] == 0:
            nps=nps+1
            print 'Relevant Sentence '+str(nps)
            print '\n'+data[p1+p2+i]+'\n' 
            out.write('\n'+str(nps)+")  "+data[p1+p2+i]+'\n')
    print("Total No. of Positive Sentences: %d" %nps)
    
    
if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding('utf8')
    classify()
 


#________________________________Extra (Please ignore)_________________________

    # bag of words transformation from raw text
#    count_vect = CountVectorizer()
#    train_ngram = count_vect.fit_transform(trn_data)
        
#    clf = svm.SVC(kernel='linear', C=1)
#    trn_predict = cross_validation.cross_val_predict(clf, train_trigram, trn_cat, cv=10)
#    trn_predict = list(trn_predict)
#    score=f1_score(trn_predict, trn_cat)
#    print 'F1 Score:'+str(score)

#    SVM by train (60%) test split (40%)
#    X_train, X_test, y_train, y_test = cross_validation.train_test_split(train_trigram, trn_cat, train_size=138, random_state=0)
#    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
#    scr=clf.score(X_test, y_test)
#    print scr   
    
#    docs_new = ['heart failure due to ejection fraction', 'many males were suffering from heart disease']
#    new_counts = count_vect.transform(docs_new)    
#    predicted = clf.predict(new_counts)
#    print predicted
#    for doc, category in zip(docs_new, predicted):
#        print doc+' belongs to '+str(category)    

#   Cross Validation on the training set to fix the C parameter  
#    scores = cross_validation.cross_val_score(clf, train_trigram, trn_cat, cv=10,scoring='f1')
##    print scores
#    print("F-measure (training set only): %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#    trn_pred = cross_validation.cross_val_predict(clf, train_trigram, trn_cat, cv=10)
#    cnfm=confusion_matrix(trn_pred,trn_cat)  
#    print cnfm
#    print f1_score(trn_pred,trn_cat)    



# Fixing the value of parameter C of SVM by Cross Validation on the training set 
#def fix_cval(train_trigram,trn_cat,val,frac):
#    fm=[];
#    if val==0.0:
#        val=0.1
#    k=val
#    for i in range (1,10):
#        clf = svm.SVC(kernel='linear', C=k, class_weight='balanced')
#        trn_pred = cross_validation.cross_val_predict(clf, train_trigram, trn_cat, cv=10)
#        fm.append(f1_score(trn_pred,trn_cat))
#        k=k+(1/frac) 
#    ind=fm.index(max(fm))
#    if frac==1:
#        cval=(int(ind))/frac
#    else:    
#        cval=val+(int(ind))/frac
##    print("cval for frac = %d: %f" %(frac,cval)) 
#    
#    if(frac!=1000):
#        frac=frac*10
#        return fix_cval(train_trigram,trn_cat,cval,frac)
#    else:
#        print("Fixed Value of C: %f" %cval)
#        return cval


              