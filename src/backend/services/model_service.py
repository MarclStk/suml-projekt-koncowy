import os
import joblib
import numpy as np
from typing import Dict, Any, Tuple, List, Optional
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV

from src.backend.data.dataset import DatasetLoader
from src.backend.domain.models import LaptopSpecification, PricePrediction


class ModelService:

    def __init__(self, model_dir: str = "/tmp", dataset_loader: Optional[DatasetLoader] = None):

        self.model_dir = model_dir
        self.model = None
        self.dataset_loader = dataset_loader if dataset_loader else DatasetLoader()

        os.makedirs(self.model_dir, exist_ok=True)

    def train_model(self, model_type: str = "random_forest") -> Dict[str, float]:
        X_train, X_test, y_train, y_test, feature_names = self.dataset_loader.prepare_train_test_data()

        if model_type == "linear":
            self.model = LinearRegression()
        elif model_type == "gradient_boosting":
            self.model = GradientBoostingRegressor(random_state=42)
        else:
            self.model = RandomForestRegressor(random_state=42, n_estimators=100)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        model_path = os.path.join(self.model_dir, f"{model_type}_model.joblib")
        joblib.dump(self.model, model_path)

        return {
            "model_type": model_type,
            "mse": mse,
            "rmse": np.sqrt(mse),
            "r2": r2
        }

    def find_best_model(self) -> Dict[str, Any]:
        X_train, X_test, y_train, y_test, feature_names = self.dataset_loader.prepare_train_test_data()

        models = {
            "linear": {
                "model": LinearRegression(),
                "params": {}
            },
            "random_forest": {
                "model": RandomForestRegressor(random_state=42),
                "params": {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [None, 10, 20]
                }
            },
            "gradient_boosting": {
                "model": GradientBoostingRegressor(random_state=42),
                "params": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 0.2]
                }
            }
        }

        best_model_info = {
            "model_type": None,
            "model": None,
            "rmse": float('inf'),
            "r2": -float('inf')
        }

        for model_name, model_info in models.items():
            print(f"Training {model_name}...")

            if model_info["params"]:
                grid_search = GridSearchCV(
                    model_info["model"],
                    model_info["params"],
                    cv=5,
                    scoring="neg_mean_squared_error",
                    n_jobs=-1
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                best_params = grid_search.best_params_
            else:
                best_model = model_info["model"]
                best_model.fit(X_train, y_train)
                best_params = {}

            y_pred = best_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)

            print(f"{model_name} - RMSE: {rmse:.2f}, R²: {r2:.2f}")

            if r2 > best_model_info["r2"]:
                best_model_info = {
                    "model_type": model_name,
                    "model": best_model,
                    "params": best_params,
                    "rmse": rmse,
                    "r2": r2
                }

        best_model_path = os.path.join(self.model_dir, "best_model.joblib")
        joblib.dump(best_model_info["model"], best_model_path)
        self.model = best_model_info["model"]

        return best_model_info

    def load_model(self, model_name: str = "best_model") -> bool:
        model_path = os.path.join(self.model_dir, f"{model_name}.joblib")

        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            return True
        else:
            return False

    def predict_price(self, laptop_spec: LaptopSpecification) -> PricePrediction:
        if self.model is None:
            if not self.load_model():
                self.train_model()

        input_data = {
            "company": laptop_spec.company,
            "product": laptop_spec.product,
            "type": laptop_spec.type_name,
            "screen_size": laptop_spec.screen_size,
            "screen_resolution": laptop_spec.screen_resolution,
            "cpu": laptop_spec.cpu,
            "ram": laptop_spec.ram,
            "gpu": laptop_spec.gpu,
            "operating_system": laptop_spec.operating_system,
            "weight": laptop_spec.weight
        }

        X = self.dataset_loader.transform_input_data(input_data)

        predicted_price = self.model.predict([X])[0]

        confidence_interval = None
        if hasattr(self.model, 'estimators_'):
            try:
                predictions = []
                for tree in self.model.estimators_:
                    predictions.append(tree.predict([X])[0])

                lower = np.percentile(predictions, 2.5)
                upper = np.percentile(predictions, 97.5)
                confidence_interval = (lower, upper)
            except:
                pass

        return PricePrediction(
            predicted_price=predicted_price,
            confidence_interval=confidence_interval
        )
