
import streamlit as st
import os

from src.backend.domain.models import LaptopSpecification, PricePrediction, LaptopCategory
from src.backend.services.pdf_service import PDFService


def render_prediction_results(
    laptop_spec: LaptopSpecification, 
    price_prediction: PricePrediction,
    category: LaptopCategory,
    pdf_service: PDFService
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
    
    if price_prediction.confidence_interval:
        lower, upper = price_prediction.confidence_interval
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px; color: #dddddd;">
            <p>Price range: {price_prediction.currency} {lower:.2f} - {price_prediction.currency} {upper:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([1, 4])
    
    with col1:
        try:
            pdf_path = pdf_service.generate_report(
                laptop_spec=laptop_spec,
                price_prediction=price_prediction,
                category=category
            )

            st.session_state.app_state["last_action"] = "pdf_download"

            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()

            st.download_button(
                label="📄 Generate & Download PDF",
                data=pdf_data,
                file_name=f"laptop_prediction_{laptop_spec.product.replace(' ', '_')}.pdf",
                mime="application/pdf",
                key="generate_download_pdf_btn"
            )
            
        except Exception as e:
            st.error(f"Error with PDF: {str(e)}")
            if "Permission denied" in str(e):
                st.info("💡 Try closing any open PDF files and try again.")
            elif "No such file" in str(e):
                st.info("💡 The output directory might be missing. Trying to create it...")
                os.makedirs("outputs", exist_ok=True)
                st.info("Please try again.")
            else:
                st.info("💡 This could be a temporary issue. Try refreshing the page.")
    
    
    with col2:
        st.info("Export the prediction to a PDF report for sharing or future reference.")
