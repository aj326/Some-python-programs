from movielib.model import MoviePersistence
import MyMovie

class MovieText(MoviePersistence.MoviePersistence):
    def loadMovies(self):
      movies = []
      try:
        f = open(self.filename, 'r')
        movieline = f.readlines()
        f.closed
        for line in movieline:
          upcs = MyMovie.MyMovie()
          if line != movieline[0]:
            upc, title, rating, year, stars, directors, genres = line.split('\t')
            stars = stars.split('/'); directors = directors.split('/'); genres = genres.split('/')
            #upcs = {'upc': upc, 'directors': directors, 'genres': genres, 'rating': rating, 'stars': stars, 'title': title, 'year': year}
            upcs['upc']=upc; upcs['directors']=directors; upcs['genres']=genres; upcs['rating']=rating
            upcs['stars']=stars; upcs['title']=title; upcs['year']=year
            movies.append(upcs)
      except IOError:
        print "File %s does not exist!" % self.filename

      return movies
        
    def saveMovies(self, movies):
      try:
        f = open(self.filename, 'w')
        toSave = 'upc\ttitle\trating\tyear\tstars\tdirectors\tgenres\n'
        for upc in movies:
          toSave += '\t'.join( [upc, movies[upc]['title'], movies[upc]['rating'], movies[upc]['year'], '/'.join(movies[upc]['stars']), '/'.join(movies[upc]['directors']), '/'.join(movies[upc]['genres'])] )
        f.write(toSave)
        f.closed
      except IOError:
        print "File %s does not exist!" % 'tester.txt'
