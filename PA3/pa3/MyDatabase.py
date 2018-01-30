from movielib.model import Database
import re
class MyDatabase(Database.Database):
    def simpleSearch(self, attribute, searchString):
      results = []
      for upc, movie in self.items():
        value = movie[attribute]
        # search multi-valued attributes
        if type(value) is list:
            for val in value:
                if searchString in val:
                    results.append((upc, movie))
        # search single-valued attributes
        elif searchString in str(value):
            results.append((upc, movie))
      return results
        
    def regexSearch(self, attribute, regex):
      results = []
      for upc, movie in self.items():
        value = movie[attribute]
        # search multi-valued attributes
        if type(value) is list:
            for val in value:
                if regex.search(val):
                    results.append((upc, movie))
        # search single-valued attributes
        elif regex.search(str(value)):
            results.append((upc, movie))
      return results
        
    def sort(self, sortAttr='upc'):
      result = []
      order = sorted(self.keys())
      for upc in order:
        result.append(self[upc])
      return result