import streamlit as st
import pickle
import pandas as pd

movie_dict = pickle.load(open("movie_dict.pkl", 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open("similarity.pkl",'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # index fetch karenge
    similar_movies = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[
                     1:6]  # sabse kam distance wali movies
    recommended_movies = []
    for i in similar_movies:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


st.title("Movie Recommendation System")

selected_movie_name = st.selectbox("Select a Movie", movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)


