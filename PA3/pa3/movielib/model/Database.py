from MovieException import MovieException

class Database(dict):
    def __init__(self, storageManager, schema, MovieClass):
        self.storageManager = storageManager
        self.schema = schema
        self.MovieClass = MovieClass
        
    def loadMovies(self):
        '''Load movies'''
        self.populate(self.storageManager.loadMovies())
        
    def saveMovies(self):
        '''Save movies'''
        self.storageManager.saveMovies(self)

    def populate(self, movies):
        '''Given a list of Movie instances, adds the mapping m['upc'] -> m for each m in the list'''
        self.clear()
        for movie in movies:
            try:
                self[movie['upc']] = movie
            except KeyError:
                raise MovieException('Error trying to add a movie without a UPC')
            
    def newMovie(self):
        return self.MovieClass()
                
    def simpleSearch(self, attribute, searchString):
        '''Given an attribute (e.g., UPC, stars, etc.) and a searchString, 
returns a list of all the movies in the database whose attribute contains the searchString.'''
        raise NotImplementedError('You must override simpleSearch')
        
    def regexSearch(self, attribute, regex):
        '''Given an attribute (e.g., UPC, stars, etc.) and a regular expression object (regex), 
returns a list of all the movies in the database whose attribute contains a substring that matches regex.'''
        raise NotImplementedError('You must override regexSearch')
        
    def sort(self, sortAttr='upc'):
        '''Returns a list of the movies in the database, sorted by the (optionally) provided attribute.
If no attribute is provided, the returned list will be sorted by UPC.'''
        raise NotImplementedError('You must override sort')
        
