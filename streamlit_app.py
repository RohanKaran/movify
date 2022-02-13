import bz2
import json
import os
import pickle
from urllib.request import urlopen
import streamlit as st
from kaggle.api import KaggleApi


@st.experimental_memo(ttl=86400)
def fetchDataFromKaggle():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='movie-recommendation-system')
    df = pickle.load(urlopen(link['files'][0]['url']))
    sm = pickle.load(bz2.BZ2File(urlopen(link['files'][1]['url']), 'rb'))
    return df, sm


def movieOrWebSeries(js):
    for key in js:
        if len(js[key]) != 0:
            return str(key)
    return False


def main():
    # setting streamlit config
    st.set_page_config(
        page_title="Movify",
        page_icon="Ⓜ",
        menu_items={
            'Get Help': 'https://linkedin.com/in/rohankaran001',
            'About':
                '''
                ## Movify 
                #### Content based movie recommendation system
                '''
        }
    )

    st.title("Movify")
    f, similarity_mat = fetchDataFromKaggle()
    tmdb_ak = os.getenv('TMDB_API_KEY', 'None')
    poster_path = 'https://api.themoviedb.org/3/find/{}?api_key=' + tmdb_ak + '&external_source=imdb_id'

    movie = st.selectbox('Search for a movie', options=f['primaryTitle'].values, index=len(f) - 1)
    st.header("\n")

    # recommendation by getting value from similarity matrix
    movie = f[f.primaryTitle == movie]
    movie_index = movie.index[len(movie) - 1]
    distances = similarity_mat[movie_index]
    mlist = sorted(list(enumerate(distances)), reverse=True, key=lambda item: item[1])[1:21]

    mlist = dict(mlist)

    for key in mlist:
        mlist[key] *= f.iloc[key].popularity
    mlist = dict(sorted(mlist.items(), reverse=True, key=lambda item: item[1]))

    result = []
    for i in mlist:
        result.append([f.iloc[i].tconst, f.iloc[i].primaryTitle])

    col_in0, col_in1 = st.columns(2)

    with col_in0:
        api = urlopen(poster_path.format(f.iloc[movie_index].tconst))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

    with col_in1:
        api = urlopen(poster_path.format(f.iloc[movie_index].tconst))
        jobj = json.load(api)

        st.subheader(f.iloc[movie_index].primaryTitle)

        overview = jobj[movieOrWebSeries(jobj)][0]["overview"]
        st.write(overview)
        try:
            rd = str(jobj[movieOrWebSeries(jobj)][0]["release_date"])
        except KeyError:
            rd = str(jobj[movieOrWebSeries(jobj)][0]["first_air_date"])
        st.write("Release Date : &nbsp;" + rd)
        rating = str(jobj[movieOrWebSeries(jobj)][0]["vote_average"])
        st.write("Rating : &nbsp;" + rating + "⭐")

    st.title("\n")
    # recommendations show
    st.subheader("Recommendations for you")
    st.subheader("\n")

    # columns
    col0, col1, col2, col3, col4 = st.columns(5)

    with col0:
        api = urlopen(poster_path.format(result[0][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[0][1])

    with col1:
        api = urlopen(poster_path.format(result[1][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[1][1])

    with col2:
        api = urlopen(poster_path.format(result[2][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[2][1])

    with col3:
        api = urlopen(poster_path.format(result[3][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[3][1])

    with col4:
        api = urlopen(poster_path.format(result[4][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[4][1])

    st.write("\n")
    col5, col6, col7, col8, col9 = st.columns(5)

    with col5:
        api = urlopen(poster_path.format(result[5][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[5][1])

    with col6:
        api = urlopen(poster_path.format(result[6][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[6][1])

    with col7:
        api = urlopen(poster_path.format(result[7][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[7][1])

    with col8:
        api = urlopen(poster_path.format(result[8][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[8][1])

    with col9:
        api = urlopen(poster_path.format(result[9][0]))
        jobj = json.load(api)
        poster = jobj[movieOrWebSeries(jobj)][0]["poster_path"]
        st.image('https://image.tmdb.org/t/p/original' + poster)

        st.write(result[9][1])


if __name__ == "__main__":
    main()
