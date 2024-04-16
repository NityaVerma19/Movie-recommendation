
import pandas as pd
import pickle
'''
movie_dict = pickle.load(open("movie_dict_img.pkl", 'rb'))
movies = pd.DataFrame(movie_dict)
movies['title'] = movies['title'].apply(lambda x: x.title())


print(movies.iloc[0])

print(movies.index)


'''
similar_movie = pickle.load(open("similar_cf.pkl", "rb"))
movie_img = pickle.load(open("movie_img.pkl", "rb"))
movie_titles = pd.DataFrame(movie_img)

values_to_delete = ["Isle of Man TT 2004 Review","Dinosaur Planet",'The Rise and Fall of ECW', "The Rise and Fall of ECW", "Paula Abdul's Get Up & Dance","8 Man","Class of Nuke 'Em High 2",
                    "Full Frame: Documentary Shorts", "Lord of the Rings: The Return of the King: Extended Edition: Bonus Material", "Nature: Antarctica",
                    "Neil Diamond: Greatest Hits Live","Screamers", "By Dawn's Early Light", "Seeta Aur Geeta", "Strange Relations", "Chump Change",
                    "Clifford: Clifford Saves the Day! / Clifford's Fluffiest Friend Cleo", "Inspector Morse 31: Death Is Now My Neighbour",
                    "Sesame Street: Elmo's World: The Street We Live On", "Lilo and Stitch", "Boycott", "Classic Albums: Meat Loaf: Bat Out of Hell",
                    "ABC Primetime: Mel Gibson's The Passion of the Christ", "Aqua Teen Hunger Force: Vol. 1", "Ashtanga Yoga: Beginner's Practice with Nicki Doane","Lady Chatterley",
                    "Zatoichi's Conspiracy", "Love Reinvented","Horror Vision","Searching for Paradise","Silent Service", "Rudolph the Red-Nosed Reindeer", "A Yank in the R.A.F."]  # Example list of values to delete
# Create a boolean mask to identify rows with values to delete
mask = movie_titles['Title'].isin(values_to_delete)

# Drop rows where mask is True
movie_titles.drop(movie_titles[mask].index, inplace=True)

print(movie_titles.head())





'''
from tmdbv3api import TMDb, Movie
tmdb = TMDb()
tmdb.api_key = '6d119a509b78d7d9adbaf2ca0f644541'
movie = Movie()

search = movie.search('Dinosaur Planet')


for res in search:
    print(res.id)
    print(res.title)
    print(res.overview)
    print(res.poster_path)
    print(res.vote_average)
'''