# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 22:23:11 2022

@author: viral
"""
import streamlit as st
import pandas as pd
# import pickle
# import response
import requests
import joblib

# def fetch_poster(movie_id):
#     response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=31aa6ae1fe5e604e392878a6838f80a9'.format(movie_id))
#     data=response.json()
#     print(data)
#     data['poster_path']
#     return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=31aa6ae1fe5e604e392878a6838f80a9".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommand(movie):
    movie_index=movies[movies['original_title']==movie].index[0]
    print(movie_index)
    dis=similarity[movie_index]
    movie_list=sorted(enumerate(list(dis)),reverse=True,key=lambda x:x[1])[1:6]

    reco_movie=[]
    reco_movie_poster=[]
    for i in movie_list:
        print(i)
        id=movies.iloc[i[0]]['id']
        print(id)
        reco_movie.append(movies.iloc[i[0]]['original_title'])
        reco_movie_poster.append(fetch_poster(id))
    return reco_movie,reco_movie_poster

st.title("Movie Recommendation System")
movies=pd.read_csv("movies.csv")
# movies=movies.set_index(movies['id'])
movie_list=list(movies['original_title'])
# print(movie_list)

similarity=joblib.load(open('similarity.joblib','rb'))

selected_movie=st.selectbox('Select Movie',movie_list)

# print(recommanded_movies)
if st.button("Recommand"):
    recommanded_movies,posters=recommand(selected_movie)
    Col1,Col2,Col3,Col4,Col5=st.columns(5)
    collist=[Col1,Col2,Col3,Col4,Col5]
    for i in range(len(recommanded_movies)):

        with collist[i]:
            st.text(recommanded_movies[i])
            st.image(posters[i])
