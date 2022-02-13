import bz2
import pickle
from urllib.request import urlopen
import streamlit as st
from kaggle.api import KaggleApi


@st.experimental_memo
def fetchDataFromKaggle():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='movie-recommendation-system')
    df = pickle.load(urlopen(link['files'][0]['url']))
    sm = pickle.load(bz2.BZ2File(urlopen(link['files'][1]['url']), 'rb'))
    return df, sm


def main():
    st.header("Movie Recommender")
    f, similarity_mat = fetchDataFromKaggle()
    movie = st.selectbox('Select', ['Select'] + f['primaryTitle'].values)
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
        result.append(f.iloc[i].primaryTitle)
    st.write(result)


if __name__ == "__main__":
    main()
