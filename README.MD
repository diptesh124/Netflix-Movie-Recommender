# 🎬 Movie Recommendation System

A content-based movie recommendation system built using Machine Learning that suggests similar movies based on user input. The application also displays movie posters and ratings using an external API.

---

## 🚀 Features

* 🔍 Search any movie
* 🎯 Get top 5 similar movie recommendations
* 🖼️ Display movie posters
* ⭐ Show movie ratings
* ⚡ Fast and interactive UI using Streamlit
* ❌ Handles invalid inputs gracefully

---

## 🧠 How It Works

This system uses **Content-Based Filtering**:

* Movie data (genres, keywords, cast, overview) is combined into a single feature
* Text is converted into numerical vectors using **CountVectorizer**
* Similarity between movies is calculated using **Cosine Similarity**
* Based on similarity scores, top 5 similar movies are recommended

---

## 🛠️ Tech Stack

* Python
* Pandas
* Scikit-learn
* Streamlit
* TMDB API (for posters & ratings)

---

## 📁 Project Structure

```
movie-recommender/
│
├── app/
│   └── app.py
│
├── data/
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│
├── model/
│   ├── movie_list.pkl
│   ├── similarity.pkl
│
├── notebooks/
│   └── model.ipynb
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone <your-repo-link>
cd movie-recommender
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the application

```
streamlit run app/app.py or
python -m streamlit run app/app.py
```

---

## 🔑 API Setup

This project uses **TMDB API** to fetch posters and ratings.

Steps:

1. Create an account on TMDB
2. Generate an API key
3. Replace in `app.py`:

```python
api_key = "YOUR_API_KEY_HERE"
```

---

## 📸 Screenshots

![alt text](<assets/Screenshot 2026-05-05 130555.png>)
![alt text](<assets/Screenshot 2026-05-05 130629.png>)
![alt text](<assets/Screenshot 2026-05-05 130659.png>)

---
## Generate Model Files

Run the notebook:
notebooks/model.ipynb

This will create required `.pkl` files in the model/ folder.

## 💡 Future Improvements

* 🔍 Autocomplete search (like Netflix)
* 🌐 Deploy online (Streamlit Cloud)
* 📱 Convert into Flutter mobile app
* 🤖 Hybrid recommendation system

---

## 🧑‍💻 Author

**Sanjeeb Yadav**
AI & ML | Flutter & AI Enthusiast

---

## ⭐ Acknowledgements

* TMDB for movie data API
* Kaggle for dataset

---

## 📌 Note

This is a beginner-friendly Machine Learning project built for learning and demonstration purposes.
