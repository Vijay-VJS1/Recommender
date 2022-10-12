import streamlit as st
import numpy as np
import requests,string,os
import pandas as pd
st.title("Movie Recommendations")
@st.cache
def load_model(url):
    st.title("HA")
    return data
load_model("h")
def load_model(size):
 return pd.read_feather(f"{os.getcwd()}/movie_deploy_{size}.feather")
def load_model(url):
    st.title("HA")
    return data
def Recommender():
    key = st.secrets["TMDB_KEY"]
    size='medium'
    col1,col2=st.columns([5,1])
    d3={}
    sizes=['small','medium','large']
    with col2:
        original_title = '<p style="font-family:Courier; color:White; font-size: 10px;">1</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        with st.expander('Size'):
            for x in range(3):
                d3[sizes[x]]=st.button(sizes[x])
    for x in range(3):
        if d3[sizes[x]]:
            size=sizes[x]
    ##################

    df=load_model(size)
    movies_list=df['title'].values
    movies_list=np.append(movies_list,"")
    movies_list=sorted(movies_list)
    similarity1=pd.read_feather(f'similarity1_{size}.feather')
    similarity2=pd.read_feather(f'similarity2_{size}.feather')
    ######################
    rows=5
    columns=5
    num_movies=25

    ######################
    def recommend(movie,version):
      recom_movies=[]
      recom_poster=[]
      recom_ratings=[]
      recom_id=[]
      if version==1:
        similarity=similarity1
      elif version==2:
        similarity=similarity2
      i=1
      movie_index=df[df['title'].str.lower()==movie.lower()].index[0]
      selected_id=df[df['title'].str.lower()==movie.lower()]['id']
      distance=similarity[str(movie_index)]
      movies_list=similarity1[str(movie_index)].sort_values(ascending=False)[1:num_movies+1].index
      ### Recommender
      for x in movies_list:
        recom_movies.append(df['title'][int(x)])
        recom_ratings.append(df['vote_average'][int(x)])
        recom_id.append(df['id'][int(x)])
        movie_id=df['id'][int(x)]
        response=requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={key}")
        if response.status_code==200:
          data=response.json()
          posters=[]
          for item in data['posters']:
            if item['iso_639_1']=='en':
               posters.append(item['file_path'])
          if len(posters)==0:
            posters.append(data['posters'][0]['file_path'])
        else:
          posters.append("https://images.app.goo.gl/uydHH7wNbPbJrM8i8")
        recom_poster.append("https://www.themoviedb.org/t/p/w600_and_h900_bestv2/"+posters[0])
      print(recom_movies)
      return recom_movies,recom_poster,recom_ratings,recom_id
      ### Popular
    def popular():
      popular_movies=[]
      popular_poster=[]
      popular_ratings=[]
      popular_ids=[]
      popular_list=df.sort_values(by='popularity',ascending=False)[:num_movies].index
      i=1
      for y in popular_list:
        popular_movies.append(df['title'][int(y)])
        popular_ratings.append(df['vote_average'][int(y)])
        popular_ids.append(df['id'][int(y)])
        popular_id=df['id'][int(y)]
        response=requests.get(f"https://api.themoviedb.org/3/movie/{popular_id}/images?api_key={key}")
        data=response.json()
        posters=[]
        for item in data['posters']:
           if item['iso_639_1']=='en':
               posters.append(item['file_path'])
        popular_poster.append("https://www.themoviedb.org/t/p/w600_and_h900_bestv2/"+posters[0])
        i+=1
      return popular_movies, popular_poster,popular_ratings,popular_ids



    #####
    #####App
    with col1:
      selected_movie = st.selectbox("",
                                    movies_list
                                    )
    search_similar=st.button('Search Similar')
    photo_dict={}
    rating_dict={}
    movies_dict={}
    st_list=list(string.ascii_lowercase)
    ####Popular
    sub_head=st.empty()
    sub_head.subheader('Trending Now')
    pop_names,pop_posters,pop_ratings,pop_ids=popular()
    cols = st.columns(5)
    x=0
    # for i in range(5):
    #     for row in range(rows):
    for row in range(rows):
        for i in range(columns):
          with cols[i]:
            photo_dict[st_list[x]]=st.empty()
            rating_dict[st_list[x]]=st.empty()
            movies_dict[st_list[x]]=st.empty()
            link=f"https://www.themoviedb.org/movie/{pop_ids[x]}"
            html = f"<a href='{link}'><img src='{pop_posters[x]}' style='width:130px;height:200px;'></a>"
            photo_dict[st_list[x]].markdown(html, unsafe_allow_html=True)
            name = f'<p style="font-family:Courier; color:Black; font-size: 15px;font-weight: bold;">{pop_names[x]}</p>'
            rating = f'<p style="font-family:Georgia; color:Black; font-size: 15px;font-weight: bold;">Rating: {round(pop_ratings[x],1)}</p>'
            # movies_dict[st_list[x]].markdown(name, unsafe_allow_html=True)
            rating_dict[st_list[x]].markdown(rating, unsafe_allow_html=True)
            x+=1
    ####Recommender
    x=0
    if search_similar:
      sub_head.subheader("Similiar Movies")
      link = "https://www.citypng.com/public/uploads/preview/loading-load-icon-transparent-png-11639609114lctjenyas8.png"
      html = f"<a href='{link}'><img src='{link}' style='width:130px;height:200px;'></a>"
      for row in range(rows):
        for i in range(columns):
          with cols[i]:
             photo_dict[st_list[x]].markdown(html, unsafe_allow_html=True)
             rating = f'<p style="font-family:Georgia; color:Blue; font-size: 20px;font-weight: bold;">Loading{""}</p>'
             rating_dict[st_list[x]].markdown(rating, unsafe_allow_html=True)
             x+=1
      x=0
      names, posters, ratings, ids = recommend(selected_movie, 1)
      for i in range(5):
        for row in range(rows):
          with cols[i]:
             link=f"https://www.themoviedb.org/movie/{ids[x]}"
             html = f"<a href='{link}'><img src='{posters[x]}' style='width:130px;height:200px;'></a>"
             photo_dict[st_list[x]].markdown(html, unsafe_allow_html=True)
             rating = f'<p style="font-family:Georgia; color:Blue; font-size: 20px;font-weight: bold;">Rating:{round(ratings[x],1)}</p>'
             rating_dict[st_list[x]].markdown(rating, unsafe_allow_html=True)
             x+=1

