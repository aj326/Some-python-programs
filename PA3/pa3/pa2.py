#####################################################################
#                            WARNING                                #
#####################################################################
#                                                                   #
#  This code is provided "as-is", which means there may be errors   #
#  in it. If you choose to use this program you must still check    #
#  for errors and remove any you find.                              # 
#                                                                   #
#####################################################################
import sys
import re

MOVIES_FILE = 'movies.txt'
ATTRIBUTES = ('title', 'rating', 'year', 'stars', 'directors', 'genres')

#############################################
# Disk -> Memory
#############################################
def splitDiskToMemory(txt):
    '''Helper function for multi-valued attributes in disk format'''
    vals = txt.split('/')
    results = []
    for val in vals:
        results.append(val.strip())
    return results

# the order of attributes in disk format,
# paired with a function to transform the value from disk format to memory format
DISK_TO_MEMORY = ((    'title', str),
                  (   'rating', str),
                  (     'year', int),
                  (    'stars', splitDiskToMemory),
                  ('directors', splitDiskToMemory),
                  (   'genres', splitDiskToMemory))

#############################################
# Memory -> Display
#############################################                  
def joinMemoryToDisplay(vals):
    '''Helper function for multi-valued attributes in memory format'''
    return ' | '.join(vals)
                  
# the order of attributes in display format,
# paired with a function to transform the value from memory format to display format
MEMORY_TO_DISPLAY = ((    'title', str),
                     (     'year', int),
                     ('directors', joinMemoryToDisplay),
                     (    'stars', joinMemoryToDisplay),
                     (   'rating', str),
                     (   'genres', joinMemoryToDisplay))

#############################################
# Display -> Memory
############################################# 
splitDisplayToMemory = splitDiskToMemory
                         
# the order of attributes in display format,
# paired with a function to transform the value from display format to memory format
DISPLAY_TO_MEMORY = ((    'title', str),
                     (     'year', int),
                     ('directors', splitDisplayToMemory),
                     (    'stars', splitDisplayToMemory),
                     (   'rating', str),
                     (   'genres', splitDisplayToMemory))

# regexes for validating user input                     
DISPLAY_VALIDATION = {      'upc' : re.compile(r'\d+'),
                          'title' : re.compile(r'.*'),
                           'year' : re.compile(r'\d\d\d\d'),
                      'directors' : re.compile(r'.*'),
                          'stars' : re.compile(r'.*'),
                         'rating' : re.compile(r'(G)|(PG)|(PG-13)|(R)|(NC-17)|(NR)'),
                         'genres' : re.compile(r'.*')}
                         
#############################################
# Memory -> Disk
#############################################
def joinMemoryToDisk(vals):
    '''Helper function for multi-valued attributes in memory format'''
    return '/'.join(vals)

# the order of attributes in memory format,
# paired with a function to transform the value from memory format to disk format
MEMORY_TO_DISK = ((    'title', str),
                  (   'rating', str),
                  (     'year', str),
                  (    'stars', joinMemoryToDisk),
                  ('directors', joinMemoryToDisk),
                  (   'genres', joinMemoryToDisk))

#############################################
# HELPER FUNCTIONS
#############################################                     
def getUserInput(prompt, regex, errorMsg=None):
    '''Repeatedly prompt a user for input, validate the input, print error message if necessary'''

    while True:
        result = raw_input(prompt)
        if not regex.match(result):
            if errorMsg:
                print errorMsg
            else:
                print 'Invalid format.\n\tShould have format %s' % regex.pattern
        else:
            return result  
            
def printMenu(menu):
    '''Display a list of available operations'''
    
    print
    print '*' * 80
    print 'MENU:'
    for key, value in menu.items():
        print '%4d: %s' % (key, value.__doc__)
    print '*' * 80

#############################################
# DISPLAYING (SORTED) MOVIES 
#############################################
def displayMovie(recNum, upc, movie):
    '''Display a single movie'''
    
    print '%10s: %d' % ('Record', recNum)
    print '%10s: %s' % ('UPC', upc)
    for attr, transform in MEMORY_TO_DISPLAY:
        print '%10s: %s' % (attr, transform(movie[attr]))   

def displayMovies(movies):
    '''Display all the movies in the collection'''

    for idx, (upc, movie) in enumerate(movies.items()):
        displayMovie(idx+1, upc, movie)
        print
    
def sortMovies(movies):
    '''Sort the movies by UPC'''

    upcs = sorted(movies.keys())
    for idx, upc in enumerate(upcs):
        displayMovie(idx+1, upc, movies[upc])
        print

#############################################
# ADDING / REMOVIING A MOVIE
#############################################
def addMovie(movies):
    '''Add a new movie to the collection'''
    upc = getUserInput('Enter the UPC: ', DISPLAY_VALIDATION['upc'])
    
    if upc in movies:
        print 'That movie is already in the database'
        return
        
    movie = {}
        
    for attr, transform in DISPLAY_TO_MEMORY:
        value = getUserInput('Enter value for %s: ' % attr, DISPLAY_VALIDATION[attr])
        movie[attr] = transform(value)
        
    movies[upc] = movie
            
def removeMovie(movies):
    '''Remove a movie from the collection'''
    del movies[getUserInput('Enter a UPC to delete: ', 
                            re.compile('|'.join(movies.keys())), 
                            errorMsg = 'That UPC is not in the database')]

#############################################
# LOADING / SAVING MOVIES
#############################################
def loadMovies(filename=MOVIES_FILE):
    '''Helper function to load movies from disk'''
    
    movies = {}

    try:
        f = open(filename)
    except IOError, error:
        print error
        return movies
    else:
        lines = f.readlines()
        f.close()
    
    # process each line into a movie
    # (this code assumes the movie file is in the proper format)
    for line in lines[1:]:   # skip the first line, which lists the attribute names
        attrs = line.split('\t')   
        upc = attrs.pop(0)
        movie = {}
        for (idx, (attr, transform)) in enumerate(DISK_TO_MEMORY):
            movie[attr] = transform(attrs[idx])
        movies[upc] = movie

    return movies
    
def loadMoviesMenu(movies):
    '''Load movies from disk'''
    
    results = loadMovies(MOVIES_FILE)
    print 'Loaded %d movies' % len(results)
    return results
    
def saveMovies(movies, filename=MOVIES_FILE):
    '''Save changes to disk'''
    
    attributes = ['UPC']
    for attr, transform in MEMORY_TO_DISK:
        attributes.append(attr)
        
    # this is a Python idiom for building strings
    lines = ['\t'.join(attributes)]
    
    for upc, movie in movies.items():
        movieLine = [upc]
        for attr, transform in MEMORY_TO_DISK:
            movieLine.append(transform(movie[attr]))
        lines.append('\t'.join(movieLine))
    
    try:
        f = open(filename, 'w')
    except IOError, error:
        print error
        return movies
    else:
        f.write('\n'.join(lines))
        f.close() 
   
#############################################
# SEARCHING MOVIES
#############################################
def search(movies, attribute, searchString, regexSearch=False):
    '''Helper function to search movies by key.
Return a list of (upc, movie) tuples where each movie's attribute value contains the searchString.
If regexSearch is True, then searchString is treated as a regular expression.'''
    
    results = []
    
    for upc, movie in movies.items():
        value = movie[attribute]
    
        # search multi-valued attributes
        if type(value) is list:
            for val in value:
                if (regexSearch and searchString.search(val)) or (not regexSearch and searchString in val):
                    results.append((upc, movie))
        
        # search single-valued attributes
        elif (regexSearch and searchString.search(str(value))) or (not regexSearch and searchString in str(value)):
            results.append((upc, movie))

    return results
    
def searchAndDisplay(movies, regexSearch=False):
    attribute, searchString = getQuery(regexSearch=regexSearch)
    results = search(movies, attribute, searchString, regexSearch=regexSearch)
    print '%d movie(s) matched the search criteria' % len(results)
    for idx, (upc, movie) in enumerate(results):
        print
        displayMovie(idx, upc, movie)
    
def searchKey(movies):
    '''Search movies by key'''    
    searchAndDisplay(movies, regexSearch=False)
    
def searchRegex(movies):
    '''Search movies using a regular expression'''    
    searchAndDisplay(movies, regexSearch=True)
    
def getQuery(regexSearch=False):
    '''Get a search query from the user. 
If parameter regexSearch is true, then the search strings should be a regular expression.'''
    if regexSearch:
        queryForm = 'attribute=regex'
    else:
        queryForm = 'attribute=searchvalue'
        
    while True:
        query = raw_input('Enter search query in the form %s: ' % queryForm)
        
        splits = query.split('=')
        if len(splits) < 2:
            print 'Invalid format. Could not detect attribute and query.'
            continue
        
        attribute = splits[0].strip()
        searchString = '='.join(splits[1:])    # in case the query contained '='
        
        if attribute.lower() not in ATTRIBUTES:
            print 'Invalid attribute. Valid attributes are %s' % ', '.join(ATTRIBUTES)
            continue
        
        if regexSearch:
            try:
                searchString = re.compile(searchString)
            except re.error:
                print 'Invalid regular expression'
                continue
        
        return attribute, searchString                

#############################################
    
def exit(movies):
    '''Quit the program'''
    print
    sys.exit()
        
def main():
    menu = dict(enumerate((displayMovies, sortMovies, 
                           searchKey, searchRegex, 
                           addMovie, removeMovie, 
                           loadMoviesMenu, saveMovies, 
                           exit)))
    movies = loadMoviesMenu(None)
    while True:     
        printMenu(menu)
        try:
            operation = menu[int(raw_input('Enter a choice: ' ))]
        except (KeyError, ValueError):
            print 'Invalid choice!'
        except KeyboardInterrupt:
            exit(movies)
        else:
            try:
                operation(movies)   
            except KeyboardInterrupt:    # allow user to hit Ctrl-C to return to menu at any time
                pass  
                
if __name__ == '__main__': main()

