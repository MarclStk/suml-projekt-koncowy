
import os
import sys
import logging
import streamlit.web.bootstrap
import streamlit.web.cli as cli

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

os.makedirs('models', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

if not os.path.exists(os.path.join('models', 'best_model.joblib')):
    logger.info("No trained model found. Training model...")
    from src.utils.init_model import init_models
    init_models()
    logger.info("Model trained successfully!")
else:
    logger.info("Using existing model.")

if __name__ == "__main__":
    logger.info("Starting LapiMate application...")
    sys.argv = ["streamlit", "run", "app.py", "--server.port=8501", "--browser.serverAddress=localhost"]

    cli.main()
