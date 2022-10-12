import pandas as pd
import streamlit as st
import os
from filter import *
def Download():
    st.title('Download Data With Filter')
    df=pd.read_feather(f"{os.getcwd()}/stream_tmdb_full_data1.feather")

    import streamlit.components.v1 as components
    from pandas.api.types import (
        is_categorical_dtype,
        is_datetime64_any_dtype,
        is_numeric_dtype,
        is_object_dtype,
    )

    df=df.dropna(subset='vote_count').reset_index(drop=True)
    df['vote_count']=df['vote_count'].apply(lambda x:round(x))
    df=df[['title','original_language','vote_average', 'vote_count',
        'tagline','overview','adult', 'backdrop_path', 'belongs_to_collection',
        'budget', 'genres','homepage', 'id', 'imdb_id',  'original_title',
         'popularity', 'poster_path', 'production_companies',
        'production_countries', 'release_date', 'revenue', 'runtime',
        'spoken_languages', 'status',  'video'
            ]]

    filtered_df =filter_dataframe(df)
    st.dataframe(filtered_df.sample(5000))
    to_csv = filtered_df.to_csv()
    st.download_button(label='📥 Download Current Result',
                                data=to_csv,
                                file_name= 'filtered_df.csv')
