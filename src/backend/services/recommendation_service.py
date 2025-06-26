
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

from src.backend.domain.models import LaptopSpecification, RecommendedLaptop
from src.backend.data.dataset import DatasetLoader


class RecommendationService:
    
    def __init__(self, dataset_loader: DatasetLoader = None):
        self.dataset_loader = dataset_loader or DatasetLoader()
        self.df = None
        self._load_data()
        
    def _load_data(self) -> None:
        self.df = self.dataset_loader.load_data()
    
    def _compute_similarity(self, target_spec: LaptopSpecification) -> pd.DataFrame:
        feature_cols = ['screen_size', 'ram', 'weight']
        X = self.df[feature_cols].values

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        target_features = np.array([
            target_spec.screen_size,
            target_spec.ram,
            target_spec.weight
        ]).reshape(1, -1)

        target_scaled = scaler.transform(target_features)

        similarity_scores = cosine_similarity(X_scaled, target_scaled).flatten()

        df_with_scores = self.df.copy()
        df_with_scores['similarity_score'] = similarity_scores

        cat_bonus = 0.1
        if target_spec.company in df_with_scores['company'].values:
            df_with_scores.loc[df_with_scores['company'] == target_spec.company, 'similarity_score'] += cat_bonus
            
        if target_spec.type_name in df_with_scores['type'].values:
            df_with_scores.loc[df_with_scores['type'] == target_spec.type_name, 'similarity_score'] += cat_bonus

        df_with_scores = df_with_scores.sort_values(by='similarity_score', ascending=False)
        
        return df_with_scores
    
    def get_similar_laptops(
        self, 
        target_spec: LaptopSpecification, 
        price_range: float = 0.2,
        limit: int = 5
    ) -> List[RecommendedLaptop]:

        df_similar = self._compute_similarity(target_spec)
        recommendations = []
        for _, row in df_similar.head(limit).iterrows():
            spec = LaptopSpecification(
                company=row['company'],
                product=row['product'],
                type_name=row['type'],
                screen_size=row['screen_size'],
                screen_resolution=row['screen_resolution'],
                cpu=row['cpu'],
                ram=row['ram'],
                gpu=row['gpu'],
                operating_system=row['operating_system'],
                weight=row['weight']
            )
            
            recommendation = RecommendedLaptop(
                company=row['company'],
                product=row['product'],
                specifications=spec,
                actual_price=row['price_euros'],
                similarity_score=row['similarity_score']
            )
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def filter_recommendations(
        self, 
        recommendations: List[RecommendedLaptop], 
        filters: Dict[str, Any]
    ) -> List[RecommendedLaptop]:

        filtered_recommendations = recommendations.copy()

        if filters.get('company'):
            filtered_recommendations = [r for r in filtered_recommendations 
                                       if r.company == filters['company']]
            
        if filters.get('cpu'):
            filtered_recommendations = [r for r in filtered_recommendations 
                                       if filters['cpu'].lower() in r.specifications.cpu.lower()]
            
        if filters.get('gpu'):
            filtered_recommendations = [r for r in filtered_recommendations 
                                       if filters['gpu'].lower() in r.specifications.gpu.lower()]
            
        if filters.get('ram_min'):
            filtered_recommendations = [r for r in filtered_recommendations 
                                       if r.specifications.ram >= filters['ram_min']]
            
        if filters.get('price_max'):
            filtered_recommendations = [r for r in filtered_recommendations 
                                       if r.actual_price <= filters['price_max']]
            
        return filtered_recommendations
