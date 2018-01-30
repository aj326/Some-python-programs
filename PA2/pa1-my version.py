# This is a Python comment. I wish Python had multi-
# line comments, but it doesn't. Instead, you have to put a
# "#" at the beginning of each line.
# 
# Name: Ahmed Al Jehairan       EID: aa29665
choice = 0

while choice !=4:
    print "*"*80, '''MENU: 
    0 Display all the movies in your collection 
    1 Sort movies by UPC 
    2 Add a new movie to the collection 
    3 Remove a movie from the collection 
    4 Quit the program '''
    try:
        choice = input("Enter A Choice: ")
    except:
        print "Error, please enter a nuumber between (0:4)"
    else:
        if choice in range(5):
            print "*"*80
            from movies import MOVIES# the DVD library is now available to you as the global variable MOVIES
            def update_movies():
                idx = enumerate(MOVIES)
                global mov_n_id_dict
                mov_n_id_dict = {}
                global movie_id
                for n, movie_id in idx:
                #print n," is movie: ",movie_id
                    mov_n_id_dict[n]= movie_id
        ##    print len(mov_n_id_dict)
        ##    print mov_n_id_dict
        ##    # print MOVIES[mov_n_id_dict]
        ##    print MOVIES[mov_n_id_dict[len(mov_n_id_dict)-1]]['title']
            update_movies()
            def isInLib (title):
                for i in range (len(mov_n_id_dict)):
                    if title.title() == MOVIES[mov_n_id_dict[i]]['title']:
                        print "you already have that movie in your library:"
                        pretty_print(i)
                        return True
                        
                
            def pretty_print(x): # pretty prints a movie
             '''The Output should look something like this
                        ID: ##########
                        Title: Movie Title
                        Genre(s): Action, Drama, Thriller..
                        Actor(s): actor1, actor2..
                        Year: yyyy
                        Director(s): Director(s)
                        Rating: Movie Rating
             '''
             print "ID: ", mov_n_id_dict[x]
             print "Title: ", MOVIES[mov_n_id_dict[x]]['title']
             print "Genre(s): ", MOVIES[mov_n_id_dict[x]]['genres']
             print "Actor(s): ", MOVIES[mov_n_id_dict[x]]['stars']
             print "Year: ", MOVIES[mov_n_id_dict[x]]['year']
             print "Director(s): ", MOVIES[mov_n_id_dict[x]]['directors']
             print "Rating:", MOVIES[mov_n_id_dict[x]]['rating']
             print "\n","*"*80 # this needs to be optimized (compatible with any screen size)
            def add2list(title=None, year= None, directors = 0, stars = 0, rating = None, genres = None):
                MOVIES[new_id]['title'] = title
                MOVIES[new_id]['year'] = year
                MOVIES[new_id]['directors'] = directors_list
                MOVIES[new_id]['stars'] = stars_list
                MOVIES[new_id]['rating'] = rating
                MOVIES[new_id]['genres'] = genres_list
                print "Done!\n"
                
            if choice == 0:
                for i in range (len(mov_n_id_dict)):
                    pretty_print(i)
                    if i != len(mov_n_id_dict)-1:
                        isNext = raw_input("~Next~~ Press Q to return to menu: ")
                        if isNext == "Q" or isNext =="q": break
                    else:
                        raw_input("Done!")
            if choice == 4:
                quit()
            if choice == 3:
                 for i in range (len(mov_n_id_dict)): print str(i) + " - " + MOVIES[mov_n_id_dict[i]]['title'] 
                 try:
                     mov2del = input("enter movie number to delete: ")
                 except:
                     print "Please, enter a movie number.."
                 else:
                     if mov2del in range(len(mov_n_id_dict)):
                         del MOVIES[mov_n_id_dict[mov2del]]
                         print "\nDeleted"
            if choice == 2:
                directors_list, stars_list, genres_list = [],[],[]
                new_id = str(int(movie_id)+1)
                MOVIES[new_id] = {}
                MOVIES[new_id]['title'] = ""
                MOVIES[new_id]['year'] = ""
                MOVIES[new_id]['diretors'] = None
                MOVIES[new_id]['stars'] = None
                MOVIES[new_id]['rating'] = ""
                MOVIES[new_id]['genres'] =None
                update_movies()
                #print len(mov_n_id_dict)
                #print mov_n_id_dict[len(mov_n_id_dict)-1]
                try:
                    title = raw_input("what is the title of the movie you wish to add? ")
                    while isInLib(title) == True:
                        title = raw_input("please enter a movie you don't already own..? ")

                    
                    year = input("what is the year of the movie you wish to add? ")
                    directors = input("how many directors directed this movie? ")
                    x = 0
                    for director in range(directors):
                        x = director+1
                        director = raw_input("what is the name of the director #"+str(x)+" of the movie you wish to add? ")
                        directors_list.append(director)
                    stars = input("how many stars acted in this movie? ")
                    for star in range(stars):
                        x = star+1
                        star = raw_input("what is the name of the star #"+str(x)+" of the movie you wish to add? ")
                        stars_list.append(star)
                    rating = raw_input("what is the rating of the movie you wish to add? ")
                    genres = input("how many genres in this movie? ")
                    for genre in range(genres):
                        x = genre+1
                        genre = raw_input("what is the genre #"+str(x)+" of the movie you wish to add? ")
                        genres_list.append(genre)
                except NameError:
                    print "You Should input a number.."
                    del MOVIES[new_id]
                else: add2list(title,year,directors_list,stars_list,rating,genres_list)
            if choice ==1:
                movies_sorted = []
                for i in range(len(MOVIES.keys())):
                    movies_sorted.append(MOVIES.keys()[i])
                movies_sorted.sort()
                for i in range(len(movies_sorted)):
                    print  movies_sorted[i],"is movie: ", MOVIES[movies_sorted[i]]['title']
                print "Done!"
        else: print "Error, please enter a nuumber between (0:4)"
