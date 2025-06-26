
import streamlit as st
import pandas as pd
from typing import Dict, Any
import os

from src.backend.domain.models import LaptopSpecification, LaptopCategory, PricePrediction
from src.backend.data.dataset import DatasetLoader
from src.backend.services.model_service import ModelService
from src.backend.services.recommendation_service import RecommendationService
from src.backend.services.pdf_service import PDFService
from src.backend.services.currency_service import CurrencyService

from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.prediction_form import render_prediction_form
from src.frontend.components.prediction_results import render_prediction_results
from src.frontend.components.history import render_history, save_to_history
from src.frontend.components.recommendation import render_recommendations
from src.frontend.components.comparison import render_comparison


def initialize_services():
    dataset_loader = DatasetLoader()

    model_service = ModelService(dataset_loader=dataset_loader)

    recommendation_service = RecommendationService(dataset_loader)

    pdf_service = PDFService()

    currency_service = CurrencyService()
    
    return {
        "dataset_loader": dataset_loader,
        "model_service": model_service,
        "recommendation_service": recommendation_service,
        "pdf_service": pdf_service,
        "currency_service": currency_service
    }


def run_app():
    st.set_page_config(
        page_title="LapiMate - Laptop Price Prediction",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    params = st.experimental_get_query_params()
    if "page" in params:
        page = params["page"][0]
    else:
        page = "prediction"

    st.title("LapiMate 💻")
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

    try:
        services["dataset_loader"].prepare_train_test_data()
        if not services["model_service"].load_model():
            st.info("Training a new model. This may take a moment...")
            services["model_service"].train_model()
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")

    selected_page, currency = render_sidebar(services["currency_service"])
    st.session_state.current_currency = currency

    selected_page = st.session_state.app_state["page"]
    
    if selected_page == "Price Prediction":
        col1, col2 = st.columns([2, 1])

        def show_saved_prediction():
            if st.session_state.app_state["showing_prediction"] and st.session_state.current_prediction["laptop_spec"]:
                laptop_spec = st.session_state.current_prediction["laptop_spec"]
                price_prediction = st.session_state.current_prediction["price_prediction"]
                category = st.session_state.current_prediction["category"]

                render_prediction_results(laptop_spec, price_prediction, category, services["pdf_service"])

                if st.session_state.app_state["recommendations"]:
                    st.markdown("---")
                    render_recommendations(st.session_state.app_state["recommendations"], price_prediction.currency)
                return True
            return False
        
        with col1:
            showing_saved = show_saved_prediction()

            form_result = None
            laptop_spec = None

            if not showing_saved:
                form_result = render_prediction_form(df, services["dataset_loader"])

            if form_result:
                action, laptop_spec = form_result

                if action == "compare":
                    if laptop_spec not in st.session_state.comparison_laptops:
                        st.session_state.comparison_laptops.append(laptop_spec)

                    st.success(f"✅ {laptop_spec.company} {laptop_spec.product} added to comparison!")

                    if len(st.session_state.comparison_laptops) > 1:
                        st.info("🔍 Go to 'Compare Laptops' to view comparison.")

                if action == "predict":
                    price_prediction = services["model_service"].predict_price(laptop_spec)

                    if st.session_state.current_currency != "USD":
                        conversion_rate = services["currency_service"].convert_currency(
                            1.0, "USD", st.session_state.current_currency
                        )
                        price_prediction = price_prediction.convert_currency(
                            st.session_state.current_currency, conversion_rate
                        )

                    category = LaptopCategory.categorize(laptop_spec, price_prediction.predicted_price)

                    st.session_state.current_prediction = {
                        "laptop_spec": laptop_spec,
                        "price_prediction": price_prediction,
                        "category": category
                    }

                    st.session_state.app_state["showing_prediction"] = True
                    st.session_state.app_state["form_submitted"] = True

                if action == "predict":
                    save_to_history(laptop_spec, price_prediction, category)

                if action == "predict":
                    recommendations = services["recommendation_service"].get_similar_laptops(laptop_spec)
                    st.session_state.app_state["recommendations"] = recommendations

                    render_prediction_results(laptop_spec, price_prediction, category, services["pdf_service"])

                    st.markdown("---")
                    render_recommendations(recommendations, price_prediction.currency)
        
        with col2:
            render_history()
    
    elif selected_page == "Compare Laptops":
        render_comparison(services, df)
