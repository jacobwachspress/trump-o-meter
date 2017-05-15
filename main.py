"""
This file does the core work of the project.
It should be left running on an uninterrupted computer, where it periodically reads the tweet file database and updates the output file accordingly.
"""
from statistics import mean
from sentiment import get_sentiment
from locations import get_location
from csv_parsing import read_last_nrows, dump_data
from tw_stream import KeywordListener
import time, threading
import pandas as pd, numpy as np

# Parameters
min_interval = 10 # seconds
n_most_recent = 10000

# Runtime vars
t0 = time.clock()
lock = threading.Lock()
 
listener = KeywordListener(filename='data/raw_tweet_stream.csv', keywords=['trump'], rule='and', lock=lock)
listener.begin()

i = 0
# Main loop
while True:
    if time.clock() - t0 < min_interval:
        continue
    
    print('Iteration', i)
    i+=1
   
    # read in tweets
    tweets = read_last_nrows('data/raw_tweet_stream.csv', n_most_recent, lock=lock)
    if tweets is None:
        continue
    print('Read tweet time: {} secs'.format(time.clock()-t0))

    #print('got tweets')
    # extract important parameters
    locs = [get_location(i) for i in tweets['loc'].values]
    sents = [get_sentiment(i) for i in tweets.text.values]
    mean_sentiment = mean(sents)
    mean_sentiment = ("%.2f" % mean_sentiment)
    mean_sentiment = "Mean national sentiment (-2 to 2 scale): " + mean_sentiment
    print (mean_sentiment)
    f = open('data/mean_sentiments.txt', 'w')
    f.write(mean_sentiment)
    f.close()
    
    # format data
    data = pd.DataFrame(columns=['sentiment','state'])
    data.loc[:,'sentiment'] = sents
    data.loc[:,'state'] = locs
    data = data[data.state!=np.nan] # filter out tweets without a location
    mean_by_state = data.groupby('state').sentiment.mean()
    
    print('Analysis time: {} secs'.format(time.clock()-t0))
    # dump data to file that web interface will read
    dump_data(mean_by_state)
    
    print('Iteration time: {} secs'.format(time.clock()-t0))
    t0 = time.clock()
    

listener.end()
