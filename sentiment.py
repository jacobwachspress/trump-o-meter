
import nltk
import csv


trump_pos_tweets = []
trump_neg_tweets = []



f = open('data/TrumpTweetsPositive.csv', encoding="utf8")
csv_f = csv.reader(f)

g = open('data/TrumpTweetsNegative.csv', encoding="utf8")
csv_g = csv.reader(g)

for row in csv_f:
  if row:
      trump_pos_tweets.append((row[0], 'positive'))

for row in csv_g:
  if row:
      trump_neg_tweets.append((row[0], 'negative'))  
           
tweets = []
for (words, sentiment) in trump_pos_tweets + trump_neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))
    
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

word_features = get_word_features(get_words_in_tweets(tweets))
training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)


def get_sentiment(text):
    # here put your code for analyzing a single tweet called `text'
    ProbDist = classifier.prob_classify(extract_features(text.split()))
    return (4 * ProbDist.prob('positive') - 2)

##
