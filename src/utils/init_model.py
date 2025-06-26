
import os
import sys
import pandas as pd
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.backend.services.model_service import ModelService
from src.backend.data.dataset import DatasetLoader


def init_models():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Initializing model training...")

    model_service = ModelService()

    if os.path.exists(os.path.join(model_service.model_dir, "best_model.joblib")):
        logger.info("Model already exists. Skipping training.")
        return

    logger.info("Finding best model...")
    best_model_info = model_service.find_best_model()
    
    logger.info(f"Best model: {best_model_info['model_type']}")
    logger.info(f"R² score: {best_model_info['r2']:.4f}")
    logger.info(f"RMSE: {best_model_info['rmse']:.4f}")
    
    logger.info("Model training completed and saved.")


if __name__ == "__main__":
    init_models()
