from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

from db.database import get_db
from models.product import ProductModel, ReviewModel
from schemas.product import ProductSchema
from utils.hashing import Hashing




nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def show_product(productid: int, db: Session):
    show_p = db.query(ProductModel).filter(ProductModel.id == productid).first()
    review_id = db.query(ReviewModel).filter(ReviewModel.product_id == show_p.id).all()
        
    # Menggunakan analisis sentimen untuk setiap ulasan
    reviews_with_sentiment = []
    for review in review_id:
        # Menggunakan NLTK untuk analisis sentimen
        sentiment_scores = sia.polarity_scores(review.comment)
        sentiment_score = sentiment_scores['compound']

        # Menentukan label sentimen berdasarkan skor sentimen
        if sentiment_score >= 0.05:
            sentiment_label = 'POSITIVE'
        elif sentiment_score <= -0.05:
            sentiment_label = 'NEGATIVE'
        else:
            sentiment_label = 'NEUTRAL'
        
        review_info = {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment,
            "sentiment": sentiment_label,
            "sentiment_score": sentiment_score
        }
        reviews_with_sentiment.append(review_info)

    response = {
        "id": show_p.id,
        "category": show_p.category,
        "price": show_p.price,
        "rating": show_p.rating,
        "image": show_p.image,
        "name": show_p.name,
        "description": show_p.description,
        "countInStock": show_p.countInStock,
        "reviews": reviews_with_sentiment,  
    }

    return response

class ProductService:
    @staticmethod
    def get_all_product(db: Session):
        return db.query(ProductModel).order_by(ProductModel.rating.desc()).limit(10).all()
    
    @staticmethod
    def recommend_products(db: Session) -> dict:
        products = ProductService.get_all_product(db)
        
        # convert products to dataframe
        df = pd.DataFrame([{
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "image": product.image,
            "countInStock": product.countInStock,
            "price": product.price,
            "rating": float(product.rating),
        } for product in products])

        # using model nearest neighbors
        nn_model = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute', n_jobs=-1)
        nn_model.fit(df['rating', 'price'])
        
        # get the 10 most similar products based on rating and price
        similar_indices = nn_model.kneighbors(df[['rating', 'price']].iloc[[0]], n_neighbors=10, return_distance=False)
        
        recommended_products = []
        for similar_index in similar_indices:
            similar_products = df.iloc[similar_index[1:]]
            recommended_products.extend(similar_products.to_dict(orient="record"))
        
        recommended_products.sort(key=lambda x: (-x['rating'], x['price']))
        
        top_recommended_products = recommended_products[:10]
        
        recommended_product_info = [{
            "id": product["id"],
        } for product in top_recommended_products ]
            