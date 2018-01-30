#####################################################################
#                            WARNING                                #
#####################################################################
# Ahmed Al Jehairan
# Eid: aa29665 
#                                                                   #
#####################################################################
# Functions!! #
import re
MOVIES = {}
def load_movies():
  f = open("movies.txt","r")
  for line in f.readlines():
    temp_list = [Line.rstrip('\n') for Line in line.split("\t")]
    if temp_list[0] !="UPC":
      MOVIES[temp_list[0]] = {"title":temp_list[1],"rating":temp_list[2],"year":temp_list[3],"stars":temp_list[4],"directors":temp_list[5],"genres":temp_list[6]}
  f.close()
  return MOVIES
def save_movies():
  f = open("movies.txt","w")
  f.write(str(tab_it()))
  f.close()
def search_both_modes(t=1):
  attribute = ""
  query = raw_input("Please enter attribute and searchvalue in this form \"attribute=searchvalue\" ")
  attribute = query.split("=")[0]
  searchvalue = query.split("=")[1]
  while attribute not in ["UPC","title","rating","year","stars","directors","genres"]:
    query = raw_input("Wrong attribute.. please choose A correct one: [UPC,title,rating,year,stars,directors,genres]: ")
    attribute = query.split("=")[0]
    searchvalue = query.split("=")[1]
  if t==1:#Simple Search
    print "searching..."
    for id in MOVIES:
      if attribute in ["title","rating","year"]:        
        if MOVIES[id][attribute] == searchvalue:
          print "Found!"
          print "ID:", id
          print "Title:", MOVIES[id]['title']
          print "Year:", MOVIES[id]['year']
          print "Directors:", formater(MOVIES[id]['directors'])
          print "Stars:", formater(MOVIES[id]['stars'])
          print "Genres:", formater(MOVIES[id]['genres'])
          print "Rating:", MOVIES[id]['rating']
          print "\n","*"*80

      elif attribute in ["genres","directors","stars"]:
        for atb in MOVIES[id][attribute].split("/"):
          if atb == searchvalue:
            print "Found!"
            print "ID:", id
            print "Title:", MOVIES[id]['title']
            print "Year:", MOVIES[id]['year']
            print "Directors:", formater(MOVIES[id]['directors'])
            print "Stars:", formater(MOVIES[id]['stars'])
            print "Genres:", formater(MOVIES[id]['genres'])
            print "Rating:", MOVIES[id]['rating']
            print "\n","*"*80
      elif searchvalue == id:
        print "Found!"
        print "ID:", id
        print "Title:", MOVIES[id]['title']
        print "Year:", MOVIES[id]['year']
        print "Directors:", formater(MOVIES[id]['directors'])
        print "Stars:", formater(MOVIES[id]['stars'])
        print "Genres:", formater(MOVIES[id]['genres'])
        print "Rating:", MOVIES[id]['rating']
        print "\n","*"*80
      else:
        print "Not Found",
        print "\n","*"*80
        break
      
  if t==2:#Advanced Search
    print "searching..."
    for id in MOVIES:
      if attribute in [id,"title","rating","year"]:        
        if re.search(MOVIES[id][attribute], searchvalue) != None or re.search(id, searchvalue)!= None:
          print "Found!"
          print "ID:", id
          print "Title:", MOVIES[id]['title']
          print "Year:", MOVIES[id]['year']
          print "Directors:", formater(MOVIES[id]['directors'])
          print "Stars:", formater(MOVIES[id]['stars'])
          print "Genres:", formater(MOVIES[id]['genres'])
          print "Rating:", MOVIES[id]['rating']
          print "\n","*"*80

      elif attribute in ["genres","directors","stars"]:
          for atb in MOVIES[id][attribute].split("/"):
            if re.search(atb,searchvalue)!= None:
              print "Found!"
              print "ID:", id
              print "Title:", MOVIES[id]['title']
              print "Year:", MOVIES[id]['year']
              print "Directors:", formater(MOVIES[id]['directors'])
              print "Stars:", formater(MOVIES[id]['stars'])
              print "Genres:", formater(MOVIES[id]['genres'])
              print "Rating:", MOVIES[id]['rating']
              print "\n","*"*80
      else:
        print "Not Found",
        print "\n","*"*80
        break
def test_input(upc, title, year, genres, stars, directors, rating):
  output = ""
  if re.match('\d', upc) == None:
    output =  "False UPC input"
  elif re.match('\w', title) == None:
    output =  "False Title input"
  elif re.match('\d', year) == None and len(year)>4:
    output =  "False Year input"
  for director in directors:
    if re.match('\D',director) == None:
      output =  "False Director Input"
  for genre in genres:
    if re.match('\D',genre) == None:
      output =  "False Genre Input"
  for star in stars:
    if re.match('\D',star) == None:
      output =  "False Star Input"
  if (rating not in ["G","PG","PG-13","R","NC-17","NR"]):
      output = "False Rating Input"
  else:
      output  = "All OK"
  return output

def formater(something):
  if type(something) is type("ASD"):
    list2 = something.split("/")
    return " | ".join(list2)
  else:
    output = ""
    for item in something:
      if item == something[len(something)-1]: output+=item
      else: output+= item + " | "
    return output
      
def tab_it():
  output = "UPC\ttitle\trating\tyear\tstars\tdirectors\tgenres\n"
  for i in MOVIES:
    output+= str(i)+"\t"
    output+= str(MOVIES[i]['title'])+"\t"
    output+= str(MOVIES[i]['rating'])+"\t"
    output+= str(MOVIES[i]['year'])+"\t"
    output+= str(MOVIES[i]['stars'])+"\t"
    output+= str(MOVIES[i]['directors'])+"\t"
    output+= str(MOVIES[i]['genres'])+"\t\n"
  return output
  
 
  
def display():
  isNext = ""
  x = 0
  for id in MOVIES:
    isNext = ""
    x = x+1
    print "Record: ", x
    print "ID:", id
    print "Title:", MOVIES[id]['title']
    print "Year:", MOVIES[id]['year']
    print "Directors:", formater(MOVIES[id]['directors'])
    print "Stars:", formater(MOVIES[id]['stars'])
    print "Genres:", formater(MOVIES[id]['genres'])
    print "Rating:", MOVIES[id]['rating']
    print "\n","*"*80
    isNext = raw_input("Next Movie? (Q to go back to menu)")
    if isNext is "Q" :
      break
      

def displaysorted(sortedupcs):
  x = 0
  for id in sortedupcs:
    x = x+1
    print "Record: ", x
    print "ID:", id
    print "Title:", MOVIES[id]['title']
    print "Year:", MOVIES[id]['year']
    print "Directors:", formater(MOVIES[id]['directors'])
    print "Stars:", formater(MOVIES[id]['stars'])
    print "Genres:", formater(MOVIES[id]['genres'])
    print "Rating:", MOVIES[id]['rating']
    print "\n","*"*80

def add():
  upc = raw_input("Enter the movie's UPC: ")

  if (upc in MOVIES):
    print "Error: a movie with that UPC already exists.  Remove that movie first if you are intentionally overwriting this entry."
    return

  title = raw_input("Enter the movie's title: ")

  year = (raw_input("Enter the movie's release year: "))
  
  directors = []
  while(True):
    dir = raw_input("Enter a director's name, or DONE to end the list of directors: ")
    if (dir != "DONE"):
      directors.append(dir)
    else:
      break

  stars = []
  while(True):
    star = raw_input("Enter a star's name, or DONE to end the list of stars: ")
    if (star != "DONE"):
      stars.append(star)
    else:
      break

  genres = []
  while(True):
    genre = raw_input("Enter a genre, or DONE to end the list of genres: ")
    if (genre != "DONE"):
      genres.append(genre)
    else:
      break

  rating = raw_input("Enter the movie's rating: ")
  if test_input(upc, title, year, genres, stars, directors, rating) == "All OK":
    MOVIES[upc] = { 'title': title, 'year': year, 'directors': directors, 'stars': stars, 'genres': genres, 'rating': rating }
  else:
    print test_input(upc, title, year, genres, stars, directors, rating)
def remove():
  upc = raw_input("Enter the UPC of the movie to delete: ")

  if (upc in MOVIES):
    del(MOVIES[upc])
  else:
    print "Error: no movie with that UPC."
load_movies()
# main loop
while (True):

  choice = raw_input("""MENU:
0 Display all the movies in your collection
1 Sort movies by UPC
2 Add a new movie to the collection
3 Remove a movie from the collection
4 Reload Movies
5 Save Movies
6 Simple Search
7 Advanced Search
8 Quit
Enter a choice: """)
  print

  if (choice == '0'):
    display()
  elif (choice == '1'):
    displaysorted(sorted(MOVIES.keys()))
  elif (choice == '2'):
    add()
  elif (choice == '3'):
    remove()
  elif (choice == '4'):
    load_movies()
    print "Loaded"
  elif (choice == '5'):
    save_movies()
  elif (choice == '6'):
     search_both_modes(1)
  elif (choice == '7'):
     search_both_modes(2)
  elif (choice == "8"):
      saveIt = raw_input("Do you want to save before you quit? (Y/N)")
      if saveIt == "Y": save_movies()
      print "Quitting"
      break
  else:
    print choice, "is an invalid menu option.  Please enter 0-8"
