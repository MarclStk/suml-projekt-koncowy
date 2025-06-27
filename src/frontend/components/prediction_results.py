
import os
import streamlit as st

from src.backend.domain.models import LaptopSpecification, PricePrediction, LaptopCategory


def render_prediction_results(
    price_prediction: PricePrediction,
    category: LaptopCategory
):

    st.subheader("Prediction Results")

    st.markdown(f"""
    <div style="background-color: #262730; padding: 20px; border-radius: 10px; text-align: center; 
    border: 1px solid #555555; margin: 10px 0;">
        <h2 style="color: #ffffff;">Estimated Price</h2>
        <h1 style="color: #00cc99;">{price_prediction.currency} {price_prediction.predicted_price:.2f}</h1>
        <p style="color: #dddddd;">Category: <strong style="color: #ffffff;">{category.name}</strong> - {category.description}</p>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("---")