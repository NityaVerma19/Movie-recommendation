import streamlit as st
import pickle
import pandas as pd
movie_dict = pickle.load(open("movie_dict_img.pkl", 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open("similarity.pkl",'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # index fetch karenge
    similar_movies = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[
                     1:6]  # sabse kam distance wali movies
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in similar_movies:
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(movies.iloc[i[0]].Image)
    return recommended_movie_names, recommended_movie_posters

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox("Select a Movie", movies['title'].values)

if st.button("Recommend"):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2,col3,col4,col5 = st.columns(5, gap = 'small')
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3 :
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


#-------------------------------------------------ITEM BASED COLLABORATIVE FILTERING--------------------------#

similar_movie = pickle.load(open("similar_cf.pkl", "rb"))
movie_img = pickle.load(open("movie_img.pkl", "rb"))
movie_titles = pd.DataFrame(movie_img)
def recommend_cf(movie_title):
    if movie_title in similar_movie.index:
        score = similar_movie[movie_title]*(5-2.5)
        score = score.sort_values(ascending = False)[1:6]    #recommend top 5 movies

        recommended_movie_names = score.index
        recommended_movie_posters = []

        for i in recommended_movie_names:
            if i in movie_titles['Title'].values:
                recommended_movie_posters = movie_titles[movie_titles['Title'] == i]['Image'].values[0]
    return recommended_movie_names, recommended_movie_posters

st.title("Collaborative Filtering Recommendation System")

selected_movie_name = st.selectbox("Select a Movie", movie_titles['Title'].values )

if st.button("Recommend again"):
    recommended_movie_names, recommended_movie_posters = recommend_cf(selected_movie_name)
    col1, col2,col3,col4,col5 = st.columns(5, gap = 'small')
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3 :
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])




