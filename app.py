import streamlit as st
import pickle
import pandas as pd
from tmdbv3api import TMDb, Movie
st.set_page_config(layout="wide", page_title= "Movie Recommendation", page_icon= "📽️")
tmdb = TMDb()
tmdb.api_key = '6d119a509b78d7d9adbaf2ca0f644541'
movie_api = Movie()


movie_dict = pickle.load(open("data/movie_dict_img.pkl", 'rb'))
movies = pd.DataFrame(movie_dict)
movies['title'] = movies['title'].apply(lambda x: x.title())

similarity = pickle.load(open("data/similarity.pkl",'rb'))

def get_movie_poster(title):
    search = movie_api.search(title)
    if search:
        movie_id = search[0].id
        movie_details = movie_api.details(movie_id)
        poster_path = movie_details.poster_path
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"
            return poster_url
    return None



#---------------------------------------------------CONTENT BASED-----------------------------------------------------------------#

tab1, tab2 = st.tabs(["Content Based", "Collaborative Filtering"])
with tab1:
    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        similar_movies = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in similar_movies:
            recommended_movie_names.append(movies.iloc[i[0]]['title'])
            recommended_movie_posters.append(get_movie_poster(movies.iloc[i[0]]['title']))
        return recommended_movie_names, recommended_movie_posters


    st.title("Movie Recommendation System")

    selected_movie_name = st.selectbox("Select a Movie", movies['title'].values)

    if st.button("Recommend"):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        for i in range(5):
            with locals()[f"col{i + 1}"]:
                st.subheader(recommended_movie_names[i])
                if recommended_movie_posters[i]:
                    st.image(recommended_movie_posters[i], width = 300)
                else:
                    st.write("Poster not available")
#------------------------------------------------------COLLABORATIVE-------------------------------------------------------------------------
with tab2:
    similar_movie = pickle.load(open("data/similar_cf.pkl", "rb"))
    movie_img = pickle.load(open("data/movie_img.pkl", "rb"))
    movie_titles = pd.DataFrame(movie_img)

    values_to_delete = ["Isle of Man TT 2004 Review", "Dinosaur Planet", 'The Rise and Fall of ECW',
                        "The Rise and Fall of ECW", "Paula Abdul's Get Up & Dance", "8 Man", "Class of Nuke 'Em High 2",
                        "Full Frame: Documentary Shorts",
                        "Lord of the Rings: The Return of the King: Extended Edition: Bonus Material",
                        "Nature: Antarctica",
                        "Neil Diamond: Greatest Hits Live", "Screamers", "By Dawn's Early Light", "Seeta Aur Geeta",
                        "Strange Relations", "Chump Change",
                        "Clifford: Clifford Saves the Day! / Clifford's Fluffiest Friend Cleo",
                        "Inspector Morse 31: Death Is Now My Neighbour",
                        "Sesame Street: Elmo's World: The Street We Live On", "Lilo and Stitch", "Boycott",
                        "Classic Albums: Meat Loaf: Bat Out of Hell",
                        "ABC Primetime: Mel Gibson's The Passion of the Christ", "Aqua Teen Hunger Force: Vol. 1",
                        "Ashtanga Yoga: Beginner's Practice with Nicki Doane", "Lady Chatterley",
                        "Zatoichi's Conspiracy", "Love Reinvented", "Horror Vision", "Searching for Paradise",
                        "Silent Service", "Rudolph the Red-Nosed Reindeer",
                        "A Yank in the R.A.F."]
    mask = movie_titles['Title'].isin(values_to_delete)

    movie_titles.drop(movie_titles[mask].index, inplace=True)


    # Function to recommend movies with posters
    def recommend_cf_with_posters(movie_title):
        if movie_title in similar_movie.index:
            score = similar_movie[movie_title] * (5 - 2.5)
            score = score.sort_values(ascending=False)[1:6]

            recommended_movie_titles = score.index
            recommended_movie_posters = []

            for title in recommended_movie_titles:
                # Ensure 'title' is string type, not integer index
                recommended_movie_posters.append(get_movie_poster(title))

            return recommended_movie_titles, recommended_movie_posters
        return [], []


    # Function to map your dataset movie title to TMDb movie title
    def map_to_tmdb_title(your_dataset_title):

        mapping = {
            "jaws 2": "Jaws 2",
            "jaws: the revenge ": "Jaws: The Revenge",
            "jaws 3": "Jaws 3-D",
            "deep blue sea":"Deep Blue Sea",
            "platoon": "Platoon"
            # Add more mappings as needed
        }
        return mapping.get(your_dataset_title, your_dataset_title)  # Return TMDb title if mapping exists, else return original title

    st.title("Recommendation System")

    selected_movie_name = st.selectbox("Select a Movie", movie_titles['Title'].values)

    if st.button("Recommend again"):
        recommended_movie_names, recommended_movie_posters = recommend_cf_with_posters(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5, gap='small')
        for i in range(5):
            with locals()[f"col{i+1}"]:
                st.subheader(recommended_movie_names[i])
                if recommended_movie_posters[i] != "Poster not available":
                    st.image(recommended_movie_posters[i], width = 300)
                else:
                    st.subheader(recommended_movie_posters[i])
