
import pandas as pd
import os
from typing import Dict, List, Tuple, Any
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split


class DatasetLoader:

    def __init__(self, file_path: str = None):
        self.file_path = file_path or os.path.join(os.getcwd(), "laptop_price.csv")
        self.df = None
        self.encoders = {}
        self.scaler = None

    def load_data(self) -> pd.DataFrame:
        try:
            self.df = pd.read_csv(self.file_path)
        except UnicodeDecodeError:
            encodings = ['latin1', 'cp1250', 'cp1252', 'ISO-8859-1', 'ISO-8859-2']
            for encoding in encodings:
                try:
                    self.df = pd.read_csv(self.file_path, encoding=encoding)
                    print(f"Udało się wczytać plik: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError(f"Nie udało się wczytać pliku. Wypróbowano kodowania: {encodings}")

        column_mapping = {
            'laptop_ID': 'laptop_id',
            'Company': 'company',
            'Product': 'product',
            'TypeName': 'type',
            'Inches': 'screen_size',
            'ScreenResolution': 'screen_resolution',
            'Cpu': 'cpu',
            'Ram': 'ram',
            'Memory': 'memory',
            'Gpu': 'gpu',
            'OpSys': 'operating_system',
            'Weight': 'weight',
            'Price_euros': 'price_euros'
        }
        self.df = self.df.rename(columns=column_mapping)

        if 'weight' in self.df.columns:
            self.df['weight'] = self.df['weight'].str.replace('kg', '').astype(float)

        if 'ram' in self.df.columns:
            self.df['ram'] = self.df['ram'].astype(str)
            self.df['ram'] = self.df['ram'].str.replace('GB', '').str.replace('gb', '').str.strip().astype(float)
        return self.df

    def get_unique_values(self, column: str) -> List:
        if self.df is None:
            self.load_data()
        return sorted(self.df[column].unique().tolist())

    def preprocess(self) -> Tuple[pd.DataFrame, Dict]:
        if self.df is None:
            self.load_data()

        df_processed = self.df.copy()

        df_processed.fillna({
            'screen_resolution': 'Unknown',
            'cpu': 'Unknown',
            'gpu': 'Unknown',
            'operating_system': 'Unknown'
        }, inplace=True)

        preprocessing_meta = {
            'categorical_columns': ['company', 'product', 'type', 'screen_resolution',
                                   'cpu', 'gpu', 'operating_system'],
            'numerical_columns': ['screen_size', 'ram', 'weight'],
            'target_column': 'price_euros'
        }

        return df_processed, preprocessing_meta

    def prepare_train_test_data(self, test_size: float = 0.2, random_state: int = 42) -> Tuple:
        if self.df is None:
            self.load_data()

        df_processed, preprocessing_meta = self.preprocess()

        price_column = 'price_euros'

        X = df_processed.drop([price_column], axis=1)
        y = df_processed[price_column]

        cat_cols = preprocessing_meta['categorical_columns']
        num_cols = preprocessing_meta['numerical_columns']

        X_cat = X[cat_cols]
        X_num = X[num_cols]

        self.encoders = {}
        X_cat_encoded_list = []

        for col in cat_cols:
            try:
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            except TypeError:
                encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
            col_encoded = encoder.fit_transform(X_cat[[col]])
            self.encoders[col] = {
                'encoder': encoder,
                'categories': encoder.categories_[0].tolist(),
                'feature_names': [f"{col}_{cat}" for cat in encoder.categories_[0]]
            }
            X_cat_encoded_list.append(col_encoded)

        if X_cat_encoded_list:
            X_cat_encoded = np.hstack(X_cat_encoded_list)
        else:
            X_cat_encoded = np.array([]).reshape(X.shape[0], 0)

        self.scaler = StandardScaler()
        X_num_scaled = self.scaler.fit_transform(X_num)

        X_combined = np.hstack([X_num_scaled, X_cat_encoded])

        feature_names = num_cols.copy()
        for col in cat_cols:
            feature_names.extend(self.encoders[col]['feature_names'])

        X_train, X_test, y_train, y_test = train_test_split(
            X_combined, y, test_size=test_size, random_state=random_state
        )

        return X_train, X_test, y_train, y_test, feature_names

    def transform_input_data(self, input_data: Dict[str, Any]) -> np.ndarray:

        num_data = []
        for col in ['screen_size', 'ram', 'weight']:
            num_data.append(input_data.get(col, 0))

        num_scaled = self.scaler.transform([num_data])[0]

        cat_encoded_list = []
        for col in ['company', 'product', 'type', 'screen_resolution', 'cpu', 'gpu', 'operating_system']:
            if col in self.encoders:
                value = input_data.get(col, '')

                encoder = self.encoders[col]['encoder']
                encoded = encoder.transform([[value]])[0]
                cat_encoded_list.append(encoded)

        if cat_encoded_list:
            cat_encoded = np.hstack(cat_encoded_list)
        else:
            cat_encoded = np.array([])

        X_combined = np.hstack([num_scaled, cat_encoded])

        return X_combined
