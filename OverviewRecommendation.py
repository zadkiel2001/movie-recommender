"""
Objective for overview recommendation
    use TFIDFVectorizer from scikit-learn to fit, transform overview column (make sure everything is preprocessed)
    use liner_kernel() to compute cosine similarity (find similarities between 2 movies)
    create reverse of indices and map movie titles (map title as index)
    make recommendation function
        -- get movie index
        -- get similarity score of movies linked to that movie
        -- sort movies by similarity score
        -- filter top 10 movies based on score
        -- get movie indices and return top 10 movies
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the CSV file
df = pd.read_csv("Movie_data_Preprocessed.csv", encoding_errors="replace")  # Replace with the path to your file

# Ensure there are no null values in the overview column, and fill if necessary
df['overview'] = df['overview'].fillna('')

# Initialize the TfidfVectorizer and transform the 'overview' column
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a reverse map of indices and movie titles
indices = pd.Series(df.index, index=df['original_title']).drop_duplicates()

# Recommendation function
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]  # Exclude the first movie (itself)

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['original_title'].iloc[movie_indices]


# Example usage
print(get_recommendations("the godfather"))  # Replace with a title in your dataset
