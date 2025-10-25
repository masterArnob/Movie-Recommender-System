# 🎬 Movie Recommender System (Content-Based)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![NLP](https://img.shields.io/badge/Domain-Natural%20Language%20Processing-orange.svg)
![Scikit-learn](https://img.shields.io/badge/Library-Scikit--learn-yellow.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📖 Project Overview

The **Movie Recommender System** is a **content-based recommendation model** built using Python and NLP techniques.  

---

## 🧩 Project Workflow

<p align="center">
  <img src="/assets/process_flow.png" alt="Workflow" width="850" style="border-radius:8px;">
</p>



```python
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movie_list:
        print(movies.iloc[i[0]].title)
