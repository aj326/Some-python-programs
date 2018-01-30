import cgi

class TextMovieView(object):
    def displayMovie(self, recNum, movie):
        '''Display a single movie'''

        print '%10s: %d' % ('Record', recNum)
        print movie   

    def displayMovies(self, movies):
        '''Display all the movies in the collection'''

        for idx, movie in enumerate(movies):
            self.displayMovie(idx+1, movie)
            print