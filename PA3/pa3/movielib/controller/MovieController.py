import sys
import re
    
class MovieController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def _printMenu(self, menu):
        '''Display a list of available operations'''
        
        print
        print '*' * 80
        print 'MENU:'
        for key, value in menu.items():
            print '%4d: %s' % (key, value.__doc__)
        print '*' * 80
        
    def _getUserInput(self, prompt, validate, errorMsg=lambda v: 'Invalid format'):
        '''Repeatedly prompt a user for input, validate the input, print error message if necessary'''

        while True:
            result = raw_input(prompt)
            if not validate(result):
                print '\t' + errorMsg(result)
            else:
                return result
        
    def exit(self):
        '''Exit the program'''
        print
        sys.exit()
        
    def _displayMovies(self):
        '''Display the movies'''
        self.view.displayMovies(self.model.values())
        
    def _displaySortedMovies(self):
        '''Display the movies sorted by UPC'''
        self.view.displayMovies(self.model.sort())
        
    def _searchKey(self):
        '''Search movies by key'''
        attribute, searchString = self._getQuery(regexSearch=False)
        results = self.model.simpleSearch(attribute, searchString)
        print '%d movie(s) matched the search criteria:\n' % len(results)
        self.view.displayMovies(results)
        
    def _searchRegex(self):
        '''Search movies by regular expression'''
        attribute, regex = self._getQuery(regexSearch=True)
        results = self.model.regexSearch(attribute, regex)
        print '%d movie(s) matched the search criteria:\n' % len(results)
        self.view.displayMovies(results)
        
    def _getQuery(self, regexSearch=False):
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
            
            if attribute.lower() not in self.model.schema.ATTRIBUTES:
                print 'Invalid attribute. Valid attributes are %s' % ', '.join(self.model.schema.ATTRIBUTES)
                continue
            
            if regexSearch:
                try:
                    searchString = re.compile(searchString)
                except re.error:
                    print 'Invalid regular expression'
                    continue
            
            return attribute, searchString

    def _addMovie(self):
        '''Add a new movie'''
            
        movie = self.model.newMovie()
         
        # get and validate UPC
        while True:
            upc = self._getUserInput('Enter a value for upc: ', 
                                     lambda v: v not in self.model, 
                                     lambda v: 'That UPC is already in the database.')
            if self._DISPLAY_VALIDATION['upc'][0](upc):
                movie['upc'] = upc
                break
            else:
                print '\t' + self._DISPLAY_VALIDATION['upc'][1](upc)
            
        # get and validate other attributes
        for attr, transform in self._DISPLAY_TO_MEMORY[1:]:
            validator, error = self._DISPLAY_VALIDATION[attr]
            value = self._getUserInput('Enter value for %s: ' % attr, validator, error)
            movie[attr] = transform(value)
            
        self.model[movie['upc']] = movie
        
                
    def _removeMovie(self):
        '''Remove an existing movie'''
        del self.model[self._getUserInput('Enter a UPC to delete: ', 
                                          lambda upc: upc in self.model.keys(), 
                                          lambda v: 'That UPC is not in the database')]

    # the order of attributes in display format,
    # paired with a function to transform the value from display format to memory format
    _DISPLAY_TO_MEMORY = ((      'upc', str),
                          (    'title', str),
                          (     'year', int),
                          ('directors', lambda txt: [val.strip() for val in txt.split('/')]),
                          (    'stars', lambda txt: [val.strip() for val in txt.split('/')]),
                          (   'rating', str),
                          (   'genres', lambda txt: [val.strip() for val in txt.split('/')]))

     # validating user input
    _DISPLAY_VALIDATION = {      'upc' : (lambda v: re.match(r'\d+', v),
                                          lambda v: 'Improper upc format. Should be \d+.'),
                               'title' : (lambda v: re.match(r'.*', v) is not None, 
                                          lambda v: 'Improper title format'),
                                'year' : (lambda v: re.match(r'\d\d\d\d', v) is not None, 
                                          lambda v: r'Improper year format. Should be \d\d\d\d'),
                           'directors' : (lambda v: re.match(r'.*', v) is not None, 
                                          lambda v: r'Improper directors format.'),
                               'stars' : (lambda v: re.match(r'.*', v) is not None, 
                                          lambda v: r'Improper stars format.'),
                              'rating' : (lambda v: re.match(r'(G)|(PG)|(PG-13)|(R)|(NC-17)|(NR)', v) is not None, 
                                          lambda v: r'Improper rating format. Should be (G)|(PG)|(PG-13)|(R)|(NC-17)|(NR)'),
                              'genres' : (lambda v: re.match(r'.*', v) is not None, 
                                          lambda v: r'Improper genres format.')}
            
    def _loadMovies(self):
        '''Load movies'''
        self.model.loadMovies()
        print '%d movies loaded' % len(self.model)

    def display(self):
        self._loadMovies()
        menu = dict(enumerate((self._displayMovies,
                               self._displaySortedMovies, 
                               self._searchKey, self._searchRegex, 
                               self._addMovie, self._removeMovie, 
                               self._loadMovies, self.model.saveMovies, 
                               self.exit)))
        while True:     
            self._printMenu(menu)
            try:
                operation = menu[int(raw_input('Enter a choice: ' ))]
            except (KeyError, ValueError):
                print 'Invalid choice!'
            except KeyboardInterrupt:
                self.exit()
            else:
                try:
                    operation()   
                except KeyboardInterrupt:    # allow user to hit Ctrl-C to return to menu at any time
                    pass  
