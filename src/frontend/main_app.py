
import streamlit as st
import pandas as pd
from typing import Dict, Any
import os

from src.backend.domain.models import LaptopSpecification, PricePrediction
from src.backend.data.dataset import DatasetLoader
from src.backend.services.model_service import ModelService
from src.backend.services.recommendation_service import RecommendationService
from src.backend.services.currency_service import CurrencyService

from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.prediction_form import render_prediction_form
from src.frontend.components.prediction_results import render_prediction_results
from src.frontend.components.history import render_history, save_to_history
from src.frontend.components.recommendation import render_recommendations
from src.frontend.components.comparison import render_comparison


def initialize_services():
    model_dir = '/tmp'

    if "dataset_loader" not in st.session_state:
        dataset_loader = DatasetLoader()
        df = dataset_loader.load_data()
        dataset_loader.prepare_train_test_data()
        st.session_state["dataset_loader"] = dataset_loader
    else:
        dataset_loader = st.session_state["dataset_loader"]

    if "model_service" not in st.session_state:
        model_service = ModelService(model_dir=model_dir, dataset_loader=dataset_loader)

        if model_service.load_model():
            st.session_state["model_trained"] = True
        else:
            with st.spinner("Training new model... This may take a moment..."):
                try:
                    model_info = model_service.find_best_model()
                    st.success(f"Model trained successfully! {model_info['model_type']} (R²: {model_info['r2']:.4f})")
                    st.session_state["model_info"] = model_info
                except Exception as e:
                    st.error(f"Error training model: {str(e)}")
                    st.session_state["training_error"] = str(e)
        
        st.session_state["model_service"] = model_service
    else:
        model_service = st.session_state["model_service"]

    recommendation_service = RecommendationService(dataset_loader)
    currency_service = CurrencyService()
    
    return {
        "dataset_loader": dataset_loader,
        "model_service": model_service,
        "recommendation_service": recommendation_service,
        "currency_service": currency_service
    }


def run_app():
    st.set_page_config(
        page_title="LapiMate - Laptop Price Prediction",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("LapiMate")
    st.markdown("""
    **Predict laptop prices based on specifications and find the best options for your needs.**
    
    LapiMate helps you understand laptop pricing, compare models, and make informed decisions.
    """)

    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []
    
    if "comparison_laptops" not in st.session_state:
        st.session_state.comparison_laptops = []
    
    if "current_currency" not in st.session_state:
        st.session_state.current_currency = "USD"

    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = None

    if "app_state" not in st.session_state:
        st.session_state.app_state = {
            "page": "Price Prediction",
            "showing_prediction": False,
            "showing_comparison": False,
            "recommendations": None,
            "last_action": None,
            "form_submitted": False
        }

    if "current_prediction" not in st.session_state:
        st.session_state.current_prediction = {
            "laptop_spec": None,
            "price_prediction": None,
            "category": None
        }

    services = initialize_services()

    df = services["dataset_loader"].load_data()

    selected_page, currency = render_sidebar(services["currency_service"])
    st.session_state.current_currency = currency

    selected_page = st.session_state.app_state["page"]
    
    if selected_page == "Price Prediction":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            form_result = render_prediction_form(df)

            if form_result:
                action, laptop_spec = form_result

                if action == "compare":
                    if laptop_spec not in st.session_state.comparison_laptops:
                        st.session_state.comparison_laptops.append(laptop_spec)

                    st.success(f"{laptop_spec.company} {laptop_spec.product} added to comparison!")

                    if len(st.session_state.comparison_laptops) > 1:
                        st.info("Go to 'Compare Laptops' to view comparison.")

                if action == "predict":
                    price_prediction = services["model_service"].predict_price(laptop_spec)

                    if st.session_state.current_currency != "USD":
                        conversion_rate = services["currency_service"].convert_currency(
                            1.0, "USD", st.session_state.current_currency
                        )
                        price_prediction = price_prediction.convert_currency(
                            st.session_state.current_currency, conversion_rate
                        )

                    st.session_state.current_prediction = {
                        "laptop_spec": laptop_spec,
                        "price_prediction": price_prediction
                    }

                    st.session_state.app_state["showing_prediction"] = True
                    st.session_state.app_state["form_submitted"] = True

                    save_to_history(laptop_spec, price_prediction)

                    recommendations = services["recommendation_service"].get_similar_laptops(laptop_spec)
                    st.session_state.app_state["recommendations"] = recommendations

                    render_prediction_results(price_prediction)

                    st.markdown("---")
                    render_recommendations(recommendations, price_prediction.currency)
        
        with col2:
            render_history()
    
    elif selected_page == "Compare Laptops":
        render_comparison()
