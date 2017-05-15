

from collections import deque
from io import StringIO
import pandas as pd

# add this to top of file:
import threading

# add this at bottom or anywhere after all the imports:
# Begin new function
def read_last_nrows(fname, n, lock=None):
    if lock is None:
        lock = threading.Lock()
    with lock:
        size = sum(1 for l in open(fname))
        if n > size:
            n = size
        df = pd.read_csv(fname, skiprows=range(1, size - n), encoding='latin1')
        return df
        
# End new function

def dump_data(data, destination='data/data.csv'):
    """
    data should be a pd.Series with index of state abbreviations and values of sentiments
    """
    template = pd.read_csv('data/states_raw.csv')
    template.index = template.abbreviation
    template.loc[:,'sentiment'] = 0
    for state,val in data.iteritems():
        template.loc[state,'sentiment'] += val
    template.to_csv(destination)
