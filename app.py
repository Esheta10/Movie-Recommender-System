from flask import Flask, render_template, request, jsonify
import pickle
import requests
import os
import gdown

app = Flask(__name__)

#https://drive.google.com/file/d/1DUbpNZGHKAOIpgRvNTjjWu2-7LKfxBht/view?usp=sharing
# Function to download similarity.pkl from Google Drive
def download_similarity_file():
    file_id = "1DUbpNZGHKAOIpgRvNTjjWu2-7LKfxBht"  # Replace with your file ID
    url = f"https://drive.google.com/uc?id={file_id}"
    output_path = "model/similarity.pkl"

    # Check if the file already exists
    if not os.path.exists(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        print("Downloading similarity.pkl...")
        gdown.download(url, output_path, quiet=False)
        print("similarity.pkl downloaded successfully!")


# Ensure similarity.pkl is downloaded
download_similarity_file()

# Load models and similarity matrix
movies = pickle.load(open('model/movies_df.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))
popular_movies = pickle.load(open('model/popular_movies.pkl', 'rb'))


# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


# Function to get movie recommendations
def recommend(movie):
    ind = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[ind])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_release_dates = []
    for i in distances[1:6]:  # Fetch 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

        # Ensure the correct column name for release date
        recommended_movie_release_dates.append(movies.iloc[i[0]].get('release_date', 'Unknown'))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_release_dates


@app.route('/')
def index():
    # Render the home page with the dropdown menu of movie titles
    return render_template('index.html', movies=movies['title'].values, recommendations=None)


@app.route('/recommend', methods=['POST'])
def get_recommendation():
    movie = request.form.get('movie')
    if movie:
        recommended_movie_names, recommended_movie_posters, recommended_movie_release_dates = recommend(movie)
        # Zip the names and posters in the backend
        recommendations = zip(recommended_movie_names, recommended_movie_posters, recommended_movie_release_dates)
        return render_template(
            'index.html',
            movies=movies['title'].values,
            recommendations=recommendations
        )
    else:
        return render_template(
            'index.html',
            movies=movies['title'].values,
            error="Please select a movie",
            recommendations=None
        )


# Added Route to Handle Popular Movies
@app.route('/popular_movies')
def get_popular_movies():
    try:
        # Load the popular movies data
        popular_movies = pickle.load(open('model/popular_movies.pkl', 'rb'))
        print("Hello world")

        # Process the popular movies with their poster paths for rendering
        popular_movies_list = []
        for idx, movie in popular_movies.iterrows():
            movie_data = {
                "title": movie['title'],
                "overview": movie['overview'],
                "poster": fetch_poster(movie['movie_id'])  # Fetch the poster from TMDB
            }
            popular_movies_list.append(movie_data)

        return render_template('popular_movies.html', popular_movies=popular_movies_list)

    except Exception as e:
        print(f"Error loading popular movies: {e}")
        return render_template('error.html', error="Could not load popular movies.")

@app.route('/moviebot')
def moviebot():
    return render_template('moviebot.html')


@app.route('/moviebot/recommend', methods=['POST'])
def moviebot_recommend():
    user_input = request.form.get('msg')
    if user_input:
        # Process user input to generate recommendations
        recommended_movie_names, recommended_movie_posters, recommended_movie_release_dates = recommend(user_input)

        # Return recommendations as a JSON response
        movies = [{"title": name, "poster": poster, "release_date": release_date}
                  for name, poster, release_date in
                  zip(recommended_movie_names, recommended_movie_posters, recommended_movie_release_dates)]

        return jsonify({"movies": movies})
    else:
        return jsonify({"error": "No input received"})


if __name__ == '__main__':
    app.run(debug=True)
