import nltk
from nltk.corpus import stopwords
p=open("postweets.txt","r")
postext=p.readlines()
n=open("negatweets.txt","r")
negtext=n.readlines()
temp1=[(item.strip(),'positive') for item in postext]
temp2=[(item.strip(),'negative') for item in negtext]
temp=temp1+temp2
tweetsW=[]
for(line,senti) in temp:
    words=[i.lower() for i in line.split()]
    tweetsW.append((words,senti))
def getWordsFreq(xyz):
    x=[]
    for(words,senti) in xyz:
        x.extend(words)
    x=nltk.FreqDist(x)
    return x.keys()
allwords=getWordsFreq(tweetsW)
customstopwords=['reading','helping','others','movie','book','person','feel','guy','study','vibe','coming','get','workshop','want']
allwords=[i for i in allwords if not i in stopwords.words('english')]
allwords=[i for i in allwords if not i in customstopwords]
print"--------\n"
def featureExtractor(document):
    document=set(document)
    features={}
    for i in allwords:
        features['contain(%s)'%i]=(i in document)
    return features
trainingSet=nltk.classify.apply_features(featureExtractor,tweetsW)
print trainingSet
classifier=nltk.NaiveBayesClassifier.train(trainingSet)
print "---------"
def getline():
    r=raw_input('enter a sentence')
    classifier.classify(featureExtractor(r.strip().split()))
    count=0
    count=int(raw_input("do you really think the above mentioned sentence is positive? If so enter 1,else enter 0"))
    if(count==1):
        s=open("postweets.txt","a")
        s.write(r)
        s.write("\n")
        s.close
    elif(count==0):
        t=open("negatweets.txt","a")
        t.write(r)
        t.wite("\n")
        t.close
getline()
p.close()
n.close()