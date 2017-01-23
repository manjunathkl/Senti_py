import nltk
import nltk.corpus
from nltk.corpus import stopwords

#Specify the names for positive and negative source files.
positive_file_name = 'postweets.txt'
negative_file_name = 'negtweets.txt'

def load_sources():
	p = open(positive_file_name)
	n = open(negative_file_name)
	postweets = p.readlines()
	negtweets = n.readlines()
	p.close()
	n.close()
	return postweets, negtweets

def train_classifier():

	postweets, negtweets = load_sources()

	temp1 = [(item,'positive') for item in postweets]
	temp2 = [(item,'negative') for item in negtweets]
	taggedtweets = temp1 + temp2

	tweetsW =  []
	for (line, senti) in taggedtweets:
		words = [i.lower() for i in line.split()]
		tweetsW.append((words,senti))	

	def getWordsFreq(word_list):
		x = []
		for (words, senti) in word_list:
			x.extend(words)
		x = nltk.FreqDist(x)
		return x.keys()

	all_words = getWordsFreq(tweetsW)

	custom_stopwords = ['bangalore', 'vanilla','chocolate', 'srk']

	words = [w for w in all_words if w not in stopwords.words('english')]
	words = [w for w in all_words if w not in custom_stopwords]

	def featureExtractor(document):
		document = set(document)
		features = {}
		for w in words:
			features['contains(%s)' % w] = (w in document)
		return features

	trainingSet = nltk.classify.apply_features(featureExtractor, tweetsW) #Second argument is a tokenized, labeled list

	classifier = nltk.NaiveBayesClassifier.train(trainingSet)
	return classifier, words, featureExtractor

def main():
        classifier, words, featureExtractor = train_classifier()
	print "Enter word/sentence when prompted (> ) or type /q to exit."
	while True:
                inp_word = raw_input('> ')

		#Typing /q or /Q exits
		if inp_word in ['/q','/Q']:
			exit(0)

		flag = 0
		for word in inp_word.strip().split():
			if word in words:
				flag = 1

		if flag == 0:
			print "We don't recognize this word yet. Is it positive? y[es]/n[o]/p[ass]: "
			choice = raw_input()
			if choice in ['y','Y']:
				p = open(positive_file_name,'a+')
				p.write('\n'+inp_word)
				p.close()
				print "Thanks. Your input was taken into account."
			elif choice in ['p','P']:
				pass
			else:
				n = open(negative_file_name,'a+')
				n.write('\n'+inp_word)
				n.close()
			classifier, words, featureExtractor = train_classifier()
		else:
			print classifier.classify(featureExtractor(inp_word.strip().split()))

if __name__ == '__main__':
	main()
