import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple

class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.ratings_df = None
        self.movie_similarity_matrix = None
        self.movie_to_idx = {}
        self.idx_to_movie = {}
        
    def load_sample_data(self):
        """Load sample movie and rating data"""
        # Sample movie data
        self.movies_df = pd.DataFrame({
            'movieId': list(range(1, 26)),  # 25 movies
            'title': [
                'The Shawshank Redemption', 'The Godfather', 'The Dark Knight',
                'Pulp Fiction', 'Forrest Gump', 'Inception', 'The Matrix',
                'Jurassic Park', 'Titanic', 'The Lord of the Rings',
                'Star Wars: Episode IV', 'The Silence of the Lambs',
                'Goodfellas', 'The Avengers', 'Avatar',
                'Interstellar', 'The Lion King', 'Fight Club',
                'Top Gun: Maverick', 'Oppenheimer',
                'Spider-Man: No Way Home', 'Parasite', 'La La Land',
                'The Grand Budapest Hotel', 'Mad Max: Fury Road'
            ],
            'genre': [
                'Drama', 'Crime', 'Action',
                'Crime', 'Drama', 'Sci-Fi',
                'Sci-Fi', 'Adventure', 'Romance',
                'Fantasy', 'Sci-Fi', 'Thriller',
                'Crime', 'Action', 'Sci-Fi',
                'Sci-Fi', 'Animation', 'Drama',
                'Action', 'Drama',
                'Action', 'Drama', 'Musical',
                'Comedy', 'Action'
            ],
            'year': [
                1994, 1972, 2008,
                1994, 1994, 2010,
                1999, 1993, 1997,
                2001, 1977, 1991,
                1990, 2012, 2009,
                2014, 1994, 1999,
                2022, 2023,
                2021, 2019, 2016,
                2014, 2015
            ]
        })
        
        # Expanded user ratings with more users and ratings
        ratings_data = []
        # Generate more diverse ratings for 10 users
        for user_id in range(1, 11):
            # Each user rates 6-10 random movies
            n_ratings = np.random.randint(6, 11)
            movie_ids = np.random.choice(self.movies_df['movieId'].values, n_ratings, replace=False)
            for movie_id in movie_ids:
                # Ratings between 1-5, with some bias towards higher ratings for popular movies
                rating = np.random.randint(3, 6) if movie_id <= 15 else np.random.randint(1, 6)
                ratings_data.append({
                    'userId': user_id,
                    'movieId': movie_id,
                    'rating': rating
                })
        
        self.ratings_df = pd.DataFrame(ratings_data)
        self._create_movie_mappings()
        
    def load_data(self, movies_data: pd.DataFrame, ratings_data: pd.DataFrame):
        """Load custom movie and rating data"""
        self.movies_df = movies_data
        self.ratings_df = ratings_data
        self._create_movie_mappings()
        
    def _create_movie_mappings(self):
        """Create mappings between movie IDs and matrix indices"""
        self.movie_to_idx = {movie_id: idx for idx, movie_id 
                            in enumerate(self.movies_df['movieId'])}
        self.idx_to_movie = {idx: movie_id for movie_id, idx 
                            in self.movie_to_idx.items()}
        
    def calculate_similarity_matrix(self):
        """Calculate movie similarity matrix using collaborative filtering"""
        # Create user-movie rating matrix
        rating_matrix = pd.pivot_table(
            self.ratings_df,
            values='rating',
            index='userId',
            columns='movieId',
            fill_value=0
        )
        
        # Calculate cosine similarity between movies
        self.movie_similarity_matrix = cosine_similarity(rating_matrix.T)
        
    def _calculate_genre_similarity(self, movie1_id: int, movie2_id: int) -> float:
        """Calculate genre similarity between two movies"""
        movie1 = self.movies_df[self.movies_df['movieId'] == movie1_id].iloc[0]
        movie2 = self.movies_df[self.movies_df['movieId'] == movie2_id].iloc[0]
        return 1.0 if movie1['genre'] == movie2['genre'] else 0.0
        
    def _calculate_year_similarity(self, movie1_id: int, movie2_id: int) -> float:
        """Calculate year similarity between two movies"""
        movie1 = self.movies_df[self.movies_df['movieId'] == movie1_id].iloc[0]
        movie2 = self.movies_df[self.movies_df['movieId'] == movie2_id].iloc[0]
        year_diff = abs(movie1['year'] - movie2['year'])
        return 1.0 / (1.0 + year_diff / 10.0)  # Decay factor for year difference
        
    def get_movie_recommendations(self, user_id: int, n_recommendations: int = 3,
                                genre_weight: float = 0.3,
                                year_weight: float = 0.2) -> List[Dict]:
        """Get movie recommendations for a user with genre and year preferences"""
        if self.movie_similarity_matrix is None:
            self.calculate_similarity_matrix()
            
        # Get user's ratings
        user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id]
        
        if user_ratings.empty:
            return []
            
        # Calculate recommendation scores for each movie
        recommendation_scores = np.zeros(len(self.movies_df))
        
        for _, rating in user_ratings.iterrows():
            movie_idx = self.movie_to_idx[rating['movieId']]
            base_similarity = self.movie_similarity_matrix[movie_idx]
            
            # Calculate genre and year similarities
            genre_similarities = np.array([
                self._calculate_genre_similarity(rating['movieId'], self.idx_to_movie[i])
                for i in range(len(self.movies_df))
            ])
            
            year_similarities = np.array([
                self._calculate_year_similarity(rating['movieId'], self.idx_to_movie[i])
                for i in range(len(self.movies_df))
            ])
            
            # Combine similarities with weights
            total_similarity = (
                (1 - genre_weight - year_weight) * base_similarity +
                genre_weight * genre_similarities +
                year_weight * year_similarities
            )
            
            recommendation_scores += total_similarity * rating['rating']
            
        # Create movie score pairs and sort
        movie_scores = list(enumerate(recommendation_scores))
        movie_scores = sorted(movie_scores, key=lambda x: x[1], reverse=True)
        
        # Filter out movies the user has already rated
        rated_movies = set(user_ratings['movieId'])
        recommendations = []
        
        for idx, score in movie_scores:
            movie_id = self.idx_to_movie[idx]
            if movie_id not in rated_movies:
                movie_info = self.movies_df[self.movies_df['movieId'] == movie_id].iloc[0]
                recommendations.append({
                    'movieId': movie_id,
                    'title': movie_info['title'],
                    'genre': movie_info['genre'],
                    'year': movie_info['year'],
                    'score': score
                })
                
                if len(recommendations) >= n_recommendations:
                    break
                    
        return recommendations

def main():
    # Create and initialize the recommender
    recommender = MovieRecommender()
    recommender.load_sample_data()
    
    # Calculate similarity matrix
    recommender.calculate_similarity_matrix()
    
    # Show recommendations for multiple users
    for user_id in [1, 2, 3]:
        print(f"\n{'='*80}")
        print(f"Analysis for User {user_id}")
        print('='*80)
        
        # Show user's current ratings
        user_ratings = recommender.ratings_df[recommender.ratings_df['userId'] == user_id]
        print(f"\nCurrent ratings for user {user_id}:")
        for _, rating in user_ratings.iterrows():
            movie_info = recommender.movies_df[recommender.movies_df['movieId'] == rating['movieId']].iloc[0]
            print(f"- {movie_info['title']} ({movie_info['year']}, {movie_info['genre']}): {rating['rating']} stars")
        
        # Get user's genre preferences
        genre_counts = {}
        for _, rating in user_ratings.iterrows():
            movie_info = recommender.movies_df[recommender.movies_df['movieId'] == rating['movieId']].iloc[0]
            genre = movie_info['genre']
            if genre not in genre_counts:
                genre_counts[genre] = {'count': 0, 'total_rating': 0}
            genre_counts[genre]['count'] += 1
            genre_counts[genre]['total_rating'] += rating['rating']
        
        print("\nGenre preferences:")
        for genre, stats in genre_counts.items():
            avg_rating = stats['total_rating'] / stats['count']
            print(f"- {genre}: {stats['count']} movies, average rating: {avg_rating:.1f}")
        
        # Get recommendations with different weights
        print("\nRecommendations (balanced):")
        recommendations = recommender.get_movie_recommendations(
            user_id, n_recommendations=5, genre_weight=0.3, year_weight=0.2
        )
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['title']} ({rec['year']}, {rec['genre']}) - Score: {rec['score']:.2f}")
        
        print("\nRecommendations (genre-focused):")
        recommendations = recommender.get_movie_recommendations(
            user_id, n_recommendations=5, genre_weight=0.6, year_weight=0.1
        )
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['title']} ({rec['year']}, {rec['genre']}) - Score: {rec['score']:.2f}")
        
        print("\nRecommendations (year-focused):")
        recommendations = recommender.get_movie_recommendations(
            user_id, n_recommendations=5, genre_weight=0.1, year_weight=0.6
        )
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['title']} ({rec['year']}, {rec['genre']}) - Score: {rec['score']:.2f}")

if __name__ == "__main__":
    main()