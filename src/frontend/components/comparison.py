
import streamlit as st
import pandas as pd
from typing import Dict, Any

from src.backend.domain.models import PredictionHistory


def render_comparison(services: Dict[str, Any], df: pd.DataFrame):

    st.header("Compare Laptops")
    
    if not st.session_state.comparison_laptops:
        st.info("No laptops added for comparison yet. Add laptops from the prediction page first.")

        if st.button("Go to Price Prediction"):
            st.session_state.page = "Price Prediction"
            st.experimental_rerun()
        return

    st.subheader("Selected Laptops")

    comparison_data = []
    for entry in st.session_state.comparison_laptops:
        if hasattr(entry, 'specification'):
            spec = entry.specification
            price_info = f"{entry.price_prediction.currency} {entry.price_prediction.predicted_price:.2f}"
            category_name = entry.category.name
        else:
            spec = entry
            price_info = "Not predicted"
            category_name = "Unknown"
        
        comparison_data.append({
            "Company": spec.company,
            "Product": spec.product,
            "Type": spec.type_name,
            "Price": price_info,
            "Category": category_name,
            "Screen Size": f"{spec.screen_size}\"",
            "Resolution": spec.screen_resolution,
            "CPU": spec.cpu,
            "RAM": f"{spec.ram} GB",
            "GPU": spec.gpu,
            "OS": spec.operating_system,
            "Weight": f"{spec.weight} kg"
        })

    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)

        st.subheader("Visual Comparison")

        features_to_compare = st.multiselect(
            "Select features to compare visually",
            ["RAM", "Screen Size", "Weight"],
            default=["RAM"]
        )
        
        if features_to_compare:
            chart_data = {}
            
            for feature in features_to_compare:
                if feature == "RAM":
                    chart_data[feature] = [entry.specification.ram for entry in st.session_state.comparison_laptops]
                elif feature == "Screen Size":
                    chart_data[feature] = [entry.specification.screen_size for entry in st.session_state.comparison_laptops]
                elif feature == "Weight":
                    chart_data[feature] = [entry.specification.weight for entry in st.session_state.comparison_laptops]

            labels = [f"{entry.specification.company} {entry.specification.product}" for entry in st.session_state.comparison_laptops]

            for feature, values in chart_data.items():
                chart_df = pd.DataFrame({
                    "Laptop": labels,
                    feature: values
                })

                st.bar_chart(chart_df.set_index("Laptop"))

        if st.button("Clear Comparison"):
            st.session_state.comparison_laptops = []
            st.experimental_rerun()
    else:
        st.info("No laptops selected for comparison.")
