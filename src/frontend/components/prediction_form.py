
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional

from src.backend.domain.models import LaptopSpecification
from src.backend.data.dataset import DatasetLoader


def render_prediction_form(df: pd.DataFrame, dataset_loader: DatasetLoader) -> Optional[LaptopSpecification]:

    st.header("Predict Laptop Price")
    st.markdown("Enter the specifications of the laptop you're interested in:")

    with st.form("laptop_prediction_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            def safe_get_options(column_name, default=None, numeric=False):
                try:
                    if column_name in df.columns:
                        values = df[column_name].dropna().unique().tolist()
                        if not values:
                            return [default] if default else ["Not Available"]

                        if numeric:
                            try:
                                return list(sorted([float(x) if isinstance(x, (int, float, str)) else x for x in values]))
                            except (ValueError, TypeError):
                                return sorted(values)
                        else:
                            return sorted(values)
                    else:
                        st.warning(f"Column {column_name} not found in dataset")
                        return [default] if default else ["Not Available"]
                except Exception as e:
                    st.warning(f"Error getting options for {column_name}: {str(e)}")
                    return [default] if default else ["Not Available"]

            companies = safe_get_options('company', "Generic")
            company = st.selectbox("Company", companies)

            types = safe_get_options('type', "Notebook")
            type_name = st.selectbox("Type", types)

            try:
                screen_sizes = safe_get_options('screen_size', [13.0, 17.0], numeric=True)
                min_screen = min(screen_sizes) if screen_sizes and screen_sizes[0] != "Not Available" else 13.0
                max_screen = max(screen_sizes) if screen_sizes and screen_sizes[0] != "Not Available" else 17.0
            except Exception:
                min_screen, max_screen = 13.0, 17.0
                
            screen_size = st.slider("Screen Size (inches)", 
                                   min_value=min_screen, 
                                   max_value=max_screen, 
                                   value=(min_screen + max_screen) / 2,
                                   step=0.1)

            resolutions = safe_get_options('screen_resolution', "1920x1080")
            screen_resolution = st.selectbox("Screen Resolution", resolutions)

            try:
                if 'ram' in df.columns:
                    ram_values = df['ram'].dropna().unique().tolist()

                    cleaned_ram = []
                    for val in ram_values:
                        try:
                            if isinstance(val, str):
                                val = val.replace('GB', '').replace('gb', '').strip()
                            cleaned_ram.append(float(val))
                        except (ValueError, TypeError):
                            pass

                    cleaned_ram = sorted(set(cleaned_ram))
                    
                    if cleaned_ram:
                        ram_values = cleaned_ram
                    else:
                        ram_values = [4, 8, 16, 32]
                else:
                    ram_values = [4, 8, 16, 32]
            except Exception as e:
                st.warning(f"Błąd przetwarzania RAM: {str(e)}")
                ram_values = [4, 8, 16, 32]
                
            ram = st.select_slider("RAM (GB)", options=ram_values)
        
        with col2:
            product = st.text_input("Product Name", value="Generic Laptop")

            cpus = safe_get_options('cpu', "Intel Core i5")
            cpu = st.selectbox("CPU", cpus)

            gpus = safe_get_options('gpu', "NVIDIA GeForce")
            gpu = st.selectbox("GPU", gpus)

            operating_systems = safe_get_options('operating_system', "Windows")
            operating_system = st.selectbox("Operating System", operating_systems)

            try:
                weights = safe_get_options('weight', [1.0, 3.0], numeric=True)
                min_weight = min(weights) if weights and weights[0] != "Not Available" else 1.0
                max_weight = max(weights) if weights and weights[0] != "Not Available" else 3.0
            except Exception:
                min_weight, max_weight = 1.0, 3.0
                
            weight = st.slider("Weight (kg)", 
                              min_value=min_weight, 
                              max_value=max_weight, 
                              value=(min_weight + max_weight) / 2,
                              step=0.1)

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Predict Price")
        with col2:
            add_to_comparison = st.form_submit_button("➕ Add to Comparison")

        def create_laptop_spec():
            return LaptopSpecification(
                company=company,
                product=product,
                type_name=type_name,
                screen_size=screen_size,
                screen_resolution=screen_resolution,
                cpu=cpu,
                ram=ram,
                gpu=gpu,
                operating_system=operating_system,
                weight=weight
            )

        if submitted:
            laptop_spec = create_laptop_spec()
            return ("predict", laptop_spec)

        if add_to_comparison:
            laptop_spec = create_laptop_spec()
            return ("compare", laptop_spec)
    
    return None
