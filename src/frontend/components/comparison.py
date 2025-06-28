import streamlit as st
import pandas as pd
from typing import Dict, Any



def render_comparison():
    st.header("Compare Laptops")

    if not st.session_state.get("comparison_laptops"):
        st.info("No laptops added for comparison yet. Add laptops from the prediction page first.")
        def go_to_prediction_callback():
            st.session_state.app_state["page"] = "Price Prediction"
        
        st.button("Go to Price Prediction", on_click=go_to_prediction_callback, key="go_to_prediction_btn")
        return

    st.subheader("Selected Laptops")

    comparison_data = []
    for entry in st.session_state.comparison_laptops:
        spec = entry.specification if hasattr(entry, 'specification') else entry
        price_info = (
            f"{entry.price_prediction.currency} {entry.price_prediction.predicted_price:.2f}"
            if hasattr(entry, 'price_prediction') else
            "Not predicted"
        )

        comparison_data.append({
            "Company": spec.company,
            "Product": spec.product,
            "Type": spec.type_name,
            "Price": price_info,
            "Screen Size": f"{spec.screen_size}\"",
            "Resolution": spec.screen_resolution,
            "CPU": spec.cpu,
            "RAM": f"{spec.ram} GB",
            "GPU": spec.gpu,
            "OS": spec.operating_system,
            "Weight": f"{spec.weight} kg"
        })

    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)

    st.subheader("Visual Comparison")

    features_to_compare = st.multiselect(
        "Select features to compare visually",
        ["RAM", "Screen Size", "Weight"],
        default=["RAM"]
    )

    if features_to_compare:
        labels = []
        chart_data = {feat: [] for feat in features_to_compare}

        for entry in st.session_state.comparison_laptops:
            spec = entry.specification if hasattr(entry, 'specification') else entry
            labels.append(f"{spec.company} {spec.product}")

            if "RAM" in chart_data:
                chart_data["RAM"].append(spec.ram)
            if "Screen Size" in chart_data:
                chart_data["Screen Size"].append(spec.screen_size)
            if "Weight" in chart_data:
                chart_data["Weight"].append(spec.weight)

        for feature, values in chart_data.items():
            chart_df = pd.DataFrame({
                "Laptop": labels,
                feature: values
            })
            st.bar_chart(chart_df.set_index("Laptop"))

    def clear_comparison_callback():
        st.session_state.comparison_laptops = []

    st.button("Clear Comparison", on_click=clear_comparison_callback, key="clear_comparison_btn")
