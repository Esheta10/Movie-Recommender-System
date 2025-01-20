# 🎥 Content-Based Movie Recommendation System

A Flask-based web application that provides movie recommendations using a content-based filtering approach. Users can select a movie to get recommendations, explore popular movies, and interact with a chatbot to get movie suggestions. 

---

## 🖼️ Project Overview

![![image](https://github.com/user-attachments/assets/973b9ea0-db74-46d7-8272-0d636fa9277d)
]()
r](#)  
*Add a screenshot or GIF of your application here to showcase its functionality.*

---

## 📋 Features

1. **Movie Recommendations**: 
   - Users can select a movie and receive five similar movie recommendations.
   - Recommendations include movie titles, posters, and release dates.

2. **Popular Movies Section**:
   - Displays a curated list of popular movies with posters and overviews.

3. **Chatbot Interaction**:
   - Users can interact with a bot to get personalized movie suggestions.

4. **Dynamic Movie Posters**:
   - Movie posters are fetched from The Movie Database (TMDB) API for a visually engaging experience.

5. **Robust Backend**:
   - Preprocessed data for recommendations and popular movies is efficiently managed using pickle files.

---

## 🛠️ Technologies Used

- **Backend**: Flask
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (for chatbot and dynamic updates)
- **Data Processing**: Pandas, Scikit-learn
- **API Integration**: TMDB API for movie posters
- **Utilities**: Google Drive (for file storage), `gdown` for downloading resources

---

## 📂 Project Structure

---

## 🧠 How It Works

1. **Data Preprocessing**:
   - Movie metadata is preprocessed and stored in pickle files.
   - Important features like genres, cast, and directors are combined for similarity computation.

2. **Recommendation Generation**:
   - Movies are vectorized, and cosine similarity is used to compute pairwise similarities.
   - The top 5 similar movies are recommended for the selected input.

3. **TMDB API Integration**:
   - Movie posters are dynamically fetched using TMDB API endpoints.

4. **Popular Movies**:
   - A separate section lists popular movies with additional details.


---

## ⚙️ Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/content-based-recommendation.git
   cd content-based-recommendation

2. Create a virtual environment
python -m venv venv

3. Activate the virtual environment
# For macOS/Linux:
source venv/bin/activate
# For Windows:
venv\Scripts\activate

4. Install the required dependencies
pip install -r requirements.txt

5. Run the application
python app.py

6. Open the application in your browser
# Navigate to:
http://127.0.0.1:5000/
