
import streamlit as st
from src.backend.services.currency_service import CurrencyService


def render_sidebar(currency_service: CurrencyService):

    st.sidebar.title("LapiMate")
    st.sidebar.image("https://img.icons8.com/color/96/000000/laptop--v1.png", width=100)

    st.sidebar.header("Navigation")
    page_options = ["Price Prediction", "Compare Laptops"]

    def on_page_change():
        if "navigation" in st.session_state:
            selected_page = st.session_state["navigation"]
            st.session_state.app_state["page"] = selected_page
            st.session_state.app_state["showing_prediction"] = False
            st.session_state.app_state["showing_comparison"] = False
    
    current_page_index = page_options.index(st.session_state.app_state["page"]) if st.session_state.app_state["page"] in page_options else 0
    selected_page = st.sidebar.radio("Go to", page_options, index=current_page_index, key="navigation", on_change=on_page_change)
    
    st.sidebar.markdown("---")

    st.sidebar.header("Settings")
    currencies = currency_service.get_available_currencies()
    selected_currency = st.sidebar.selectbox(
        "Currency", 
        currencies,
        index=currencies.index(st.session_state.current_currency)
    )
    

    return selected_page, selected_currency
