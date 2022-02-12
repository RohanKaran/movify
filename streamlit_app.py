import pickle
from urllib.request import urlopen
import streamlit as st
from kaggle.api import KaggleApi

# config = dotenv_values(".env")
# movies_link = config.get("MOVIES_LINK")
# crew_link = config.get("CREW_LINK")
# ratings_link = config.get("RATINGS_LINK")
# if os.getenv('MOVIES_LINK'):
#     movies_link = os.getenv("MOVIES_LINK")
#     crew_link = os.getenv("CREW_LINK")
#     ratings_link = os.getenv("RATINGS_LINK")


@st.experimental_memo
def fetchDataFromKaggle():
    api = KaggleApi()
    api.authenticate()
    link = api.kernel_output(user_name='rohankaran', kernel_slug='movie-recommendation-system')
    print(link)
    df = pickle.load(urlopen(link['files'][0]['url']))
    sm = pickle.load(urlopen(link['files'][1]['url']))
    print(df)
    return df, sm


# @st.experimental_memo
# def preProcessing():
#     movies = pd.read_csv(movies_link, sep='\t', dtype=str)
#     start = time.time()
#     print(start)
#     movies['startYear'] = movies['startYear'].replace("\\N", '0')
#     movies['startYear'] = movies['startYear'].astype(int)
#     movies['runtimeMinutes'] = pd.to_numeric(movies.runtimeMinutes, errors="coerce")
#     movies['runtimeMinutes'] = movies['runtimeMinutes'].replace(np.nan, 0)
#     movies['runtimeMinutes'] = movies['runtimeMinutes'].astype(float).astype(int)
#     movies_processed = movies[
#         ((movies.titleType == 'movie') | (movies.titleType == 'tvSeries')) & (movies.genres != '\\N')]
#
#     crews = pd.read_csv(crew_link, sep='\t', dtype=str)
#     crews['directors'] = crews['directors'].replace("\\N", '')
#     crews['writers'] = crews['writers'].replace("\\N", '')
#     crews['crews'] = crews['writers'].str.split(",") + crews['directors'].str.split(",")
#     crews = crews.drop(['writers', 'directors'], axis=1)
#     final = pd.merge(movies_processed, crews, on='tconst')
#     final['isAdult'] = final['isAdult'].replace('0', 'notadult')
#     final['isAdult'] = final['isAdult'].replace('1', 'isadult')
#     final['genres'] = final['genres'].str.split(',')
#
#     ratings = pd.read_csv(ratings_link, sep='\t', dtype={'tconst': str, 'averageRating': float, 'numVotes': int})
#     ratings['popularity'] = ratings['averageRating'] * ratings['numVotes']
#     ratings = ratings[ratings.popularity >= ratings.popularity.quantile(q=0.992)]
#     ratings_min = ratings['popularity'].min()
#     ratings_max = ratings['popularity'].max()
#     ratings['popularity'] = (ratings['popularity'] - ratings_min) / (ratings_max - ratings_min)
#     ratings = ratings.drop(['averageRating', 'numVotes'], axis=1)
#     final = pd.merge(final, ratings, on='tconst')
#     final['titleType'] = final['titleType'].str.split(',')
#     final['tags'] = final['titleType'] + final['titleType'] + final['isAdult'].str.split() + final['crews'] + final[
#         'genres']
#     print(final['tags'])
#     f = final[['tconst', 'tags', 'primaryTitle', 'popularity']]
#     f['tags'] = f['tags'].apply(lambda x: " ".join(x).lower())
#     mid = time.time()
#     print(mid - start)
#     cv = CountVectorizer(max_features=9000, token_pattern=r"\S+")
#     vectors = cv.fit_transform(f['tags']).toarray()
#     similarity_matrix = cosine_similarity(vectors)
#
#     end = time.time()
#     print(end - start)
#     return f, similarity_matrix


# print(f[f['primaryTitle'] == 'The Avengers'].index[2])
# print(f[f['primaryTitle'] == 'Avengers: Age of Ultron'])


def main():
    f, similarity_mat = fetchDataFromKaggle()
    movie = st.selectbox('Select', f['primaryTitle'].values)
    movie = f[f.primaryTitle == movie]
    movie_index = movie.index[len(movie) - 1]
    distances = similarity_mat[movie_index]
    mlist = sorted(list(enumerate(distances)), reverse=True, key=lambda item: item[1])[1:21]

    mlist = dict(mlist)

    print(mlist)
    for key in mlist:
        mlist[key] *= f.iloc[key].popularity
    mlist = dict(sorted(mlist.items(), reverse=True, key=lambda item: item[1]))

    result = []
    for i in mlist:
        result.append(f.iloc[i].primaryTitle)
    st.write(result)


if __name__ == "__main__":
    main()
