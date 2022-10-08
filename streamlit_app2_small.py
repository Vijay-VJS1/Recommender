import streamlit as st 
import numpy as np
import requests,string
import pandas as pd
key='00d9d014c90f00239dc8341d1a1bf045'
##################
df=pd.read_feather("movie_deploy_small.feather")
movies_list=df['title'].values
movies_list=np.append(movies_list,"")
movies_list=sorted(movies_list)
similarity1=pd.read_feather('similarity1_small.feather')
similarity2=pd.read_feather('similarity2_small.feather')
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
  movies_list=similarity1[str(movie_index)].sort_values(ascending=False)[1:11].index
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
  return recom_movies,recom_poster,recom_ratings,recom_id
  ### Popular
def popular():
  popular_movies=[]
  popular_poster=[]
  popular_ratings=[]
  popular_ids=[]
  popular_list=df.sort_values(by='popularity',ascending=False)[:10].index
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
st.title("Movie Recommedations")
selected_movie=st.selectbox("Search Here",
movies_list
)
search_similar=st.button('Search Similar')
d1={}
d2={}
st_list=list(string.ascii_lowercase)
####Popular
sub_head=st.empty()
sub_head.subheader("Trending Now")
pop_names,pop_posters,pop_ratings,pop_ids=popular()
cols = st.columns(5)
x=0
for i in range(5):
    for row in range(2):
      with cols[i]:
        d1[st_list[x]]=st.empty()
        d2[st_list[x]]=st.empty()
        link=f"https://www.themoviedb.org/movie/{pop_ids[i+row*5]}"
        html = f"<a href='{link}'><img src='{pop_posters[i+row*5]}' style='width:130px;height:200px;'></a>"
        d1[st_list[x]].markdown(html, unsafe_allow_html=True)
        rating = f'<p style="font-family:Georgia; color:Blue; font-size: 20px;font-weight: bold;">Rating:{round(pop_ratings[i+row*5],1)}</p>'
        d2[st_list[x]].markdown(rating, unsafe_allow_html=True)
        x+=1
####Recommender
x=0
if search_similar:
  sub_head.subheader("Similiar Movies")
  link = "https://www.citypng.com/public/uploads/preview/loading-load-icon-transparent-png-11639609114lctjenyas8.png"
  html = f"<a href='{link}'><img src='{link}' style='width:130px;height:200px;'></a>"
  for i in range(5):
    for row in range(2):
      with cols[i]:
         d1[st_list[x]].markdown(html, unsafe_allow_html=True)
         rating = f'<p style="font-family:Georgia; color:Blue; font-size: 20px;font-weight: bold;">Rating:{""}</p>'
         d2[st_list[x]].markdown(rating, unsafe_allow_html=True)
         x+=1
  x=0
  for i in range(5):
    for row in range(2):
      with cols[i]:
         names,posters,ratings,ids=recommend(selected_movie,1)
         link=f"https://www.themoviedb.org/movie/{ids[i+row*5]}"
         html = f"<a href='{link}'><img src='{posters[i+row*5]}' style='width:130px;height:200px;'></a>"
         d1[st_list[x]].markdown(html, unsafe_allow_html=True)
         rating = f'<p style="font-family:Georgia; color:Blue; font-size: 20px;font-weight: bold;">Rating:{round(ratings[i+row*5],1)}</p>'
         d2[st_list[x]].markdown(rating, unsafe_allow_html=True)
         x+=1
