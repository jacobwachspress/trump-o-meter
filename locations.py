
import pandas as pd

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# data from http://simplemaps.com/data/us-cities
all_cities = pd.read_csv('data/cities.csv', delimiter=',')
all_cities.loc[:,'city_lowercase'] = all_cities['city'].str.lower()
all_cities.loc[:,'state_uppercase'] = all_cities['state_id'].str.upper()
all_cities = all_cities[all_cities.state_uppercase.isin(states)]

big_cities = pd.read_csv('data/big_cities.csv', delimiter=',')
big_cities.loc[:,'city_lowercase'] = big_cities['city'].str.lower()
big_cities.loc[:,'state_uppercase'] = big_cities['state'].str.upper()
big_cities = big_cities[big_cities.state_uppercase.isin(states)]
bclist = list(big_cities.city_lowercase.values)
stlist = list(big_cities.state_uppercase.values)

all_countries = pd.read_csv('data/countries.csv', delimiter=',')
all_countries.loc[:, 'country'] = all_countries['name'].str.lower()

all_zip_codes = pd.read_csv('data/zip_code_database.csv', delimiter=',')
all_zip_codes.loc[:,'zip'] = all_zip_codes['zip']
all_zip_codes.loc[:,'state_uppercase'] = all_zip_codes['state'].str.upper()
all_zip_codes = all_zip_codes[all_zip_codes.state_uppercase.isin(states)]

## used later for zip-code comparisons
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

state_names = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'mebraska': 'NE',
    'nevada': 'NV',
    'hampshire': 'NH',
    'jersey': 'NJ',
    'york': 'NY',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'rhode': 'RI',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'wisconsin': 'WI',
    'wyoming': 'WY',
}


def get_location(loc):
    """
    Should return the proper abbreviation of a state
    """
    if loc is None:
        return None
    
    loc = str(loc)
    
    loc_pieces = loc.split(' ')
    loc_pieces = [l.strip(',') for l in loc_pieces]
    
    ## word in causes problems, use case here
    if ('IN' in loc_pieces):
        return 'IN'
        
    loc_pieces = [l.lower() for l in loc_pieces]


    for lp in loc_pieces:
        if len(lp)==2:
            if lp.upper() in states:
                return lp.upper()
        if (lp in state_names):
            return state_names.get(lp)
    
    if ('new' in loc_pieces) and ('mexico' in loc_pieces):
        return 'NM'
        
    if ('west' in loc_pieces) and ('virginia' in loc_pieces):
        return 'WV'
        
    if ('west' not in loc_pieces) and ('virginia' in loc_pieces):
        return 'VA'
        
    if ('washington' in loc_pieces) and not ('d.c.' in loc_pieces) and not ('dc' in loc_pieces):
        return 'WA'
        
    if ('dakota' in loc_pieces):
        if ('north' in loc_pieces):
            return 'ND'
        if ('south' in loc_pieces):
            return 'SD'
            
    if ('carolina' in loc_pieces):
        if ('north' in loc_pieces):
            return 'NC'
        if ('south' in loc_pieces):
            return 'SC'
            
    if ('nyc' in loc_pieces):
        return 'NY'
    
    if ('st.' in loc_pieces):
        if ('louis' in loc_pieces):
            return 'MO'
        if ('paul' in loc_pieces):
            return 'MN'
            
    ## test for major cities
    for lp in loc_pieces:
        
        if lp in bclist:
            idx = bclist.index(lp)
            return stlist[idx]
        



