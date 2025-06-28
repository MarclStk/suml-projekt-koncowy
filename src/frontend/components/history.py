
import streamlit as st
from datetime import datetime

from src.backend.domain.models import LaptopSpecification, PricePrediction, PredictionHistory


def save_to_history(
    laptop_spec: LaptopSpecification,
    price_prediction: PricePrediction
):

    history_entry = PredictionHistory(
        timestamp=datetime.now(),
        specification=laptop_spec,
        price_prediction=price_prediction
    )

    st.session_state.prediction_history.append(history_entry)

    if len(st.session_state.prediction_history) > 10:
        st.session_state.prediction_history = st.session_state.prediction_history[-10:]


def render_history():

    st.subheader("Recent Predictions")
    
    if not st.session_state.prediction_history:
        st.info("No prediction history yet. Make your first prediction!")
        return

    for i, entry in enumerate(reversed(st.session_state.prediction_history)):
        with st.expander(f"{entry.specification.company} {entry.specification.product}"):
            st.write(f"**Price:** {entry.price_prediction.currency} {entry.price_prediction.predicted_price:.2f}")

            st.write("**Key Specs:**")
            st.write(f"- CPU: {entry.specification.cpu}")
            st.write(f"- RAM: {entry.specification.ram} GB")
            st.write(f"- GPU: {entry.specification.gpu}")

            if st.button(f"Add to Comparison", key=f"add_compare_{i}"):
                if entry not in st.session_state.comparison_laptops:
                    st.session_state.comparison_laptops.append(entry)
                    st.success("Added to comparison!")
            
            st.write(f"Predicted on: {entry.timestamp.strftime('%Y-%m-%d %H:%M')}")

    def clear_history_callback():
        st.session_state.prediction_history = []

    st.button("Clear History", on_click=clear_history_callback, key="clear_history_btn")
