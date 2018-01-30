from movielib.model import Movie

class MyMovie(Movie.Movie):
  
  def __str__(self):
    result = '\n %10s: %s' % ('UPC', self['upc'])
    result += '\n %10s: %s' % ('Title', self['title'])
    result += '\n %10s: %s' % ('Year', self['year'])
    result += '\n %10s: %s' % ('Directors', ' | '.join(self['directors']))
    result += '\n %10s: %s' % ('Stars', ' | '.join(self['stars']))
    result += '\n %10s: %s' % ('Rating', self['rating'])
    result += '\n %10s: %s' % ('Genres', ' | '.join(self['genres']))
    return result
    