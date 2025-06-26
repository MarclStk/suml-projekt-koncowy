
import streamlit as st
from typing import List

from src.backend.domain.models import RecommendedLaptop


def render_recommendations(recommendations: List[RecommendedLaptop], currency: str):

    st.subheader("Similar Laptops You Might Like")
    
    if not recommendations:
        st.info("No recommendations found.")
        return

    st.write("Filter recommendations:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_price = st.number_input("Min Price", value=0.0, step=100.0)
    
    with col2:
        max_price = st.number_input("Max Price", value=5000.0, step=100.0)
    
    with col3:
        filter_company = st.multiselect("Companies", 
                                       list(set(r.company for r in recommendations)),
                                       default=[])

    filtered_recommendations = [
        r for r in recommendations
        if r.actual_price >= min_price
        and r.actual_price <= max_price
        and (not filter_company or r.company in filter_company)
    ]

    if not filtered_recommendations:
        st.warning("No laptops match your filters.")
        return

    cols = st.columns(min(3, len(filtered_recommendations)))
    
    for i, laptop in enumerate(filtered_recommendations[:3]):  # Show top 3
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 5px; padding: 10px; margin: 5px;">
                <h4>{laptop.company} {laptop.product}</h4>
                <p><strong>{currency} {laptop.actual_price:.2f}</strong></p>
                <p>Similarity: {int(laptop.similarity_score * 100)}%</p>
                <p><strong>Specs:</strong><br>
                CPU: {laptop.specifications.cpu}<br>
                RAM: {laptop.specifications.ram} GB<br>
                GPU: {laptop.specifications.gpu}<br>
                Screen: {laptop.specifications.screen_size}"</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Compare", key=f"compare_{i}"):
                if laptop not in st.session_state.comparison_laptops:
                    from src.backend.domain.models import PredictionHistory, PricePrediction, LaptopCategory
                    from datetime import datetime
                    
                    entry = PredictionHistory(
                        timestamp=datetime.now(),
                        specification=laptop.specifications,
                        price_prediction=PricePrediction(
                            predicted_price=laptop.actual_price,
                            currency=currency
                        ),
                        category=LaptopCategory.categorize(
                            laptop.specifications, laptop.actual_price
                        )
                    )
                    
                    st.session_state.comparison_laptops.append(entry)
                    st.success("Added to comparison!")
