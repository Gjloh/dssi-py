"""
This module automates model training for HDB rent prediction (regression).
"""

import argparse
import logging

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from src import data_processor
from src import model_registry
from src import evaluation
from src.config import appconfig

logging.basicConfig(level=logging.INFO)

features = appconfig['Model']['features'].split(',')
categorical_features = appconfig['Model']['categorical_features'].split(',')
label = appconfig['Model']['label']

def run(data_path):
    logging.info('Process Data...')
    df = data_processor.run(data_path)

    # Preprocessor: one-hot encode categorical features, pass through others
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")
    preprocessor = ColumnTransformer(
        transformers=[("cat", categorical_transformer, categorical_features)],
        remainder='passthrough'
    )

    # Train-Test Split
    logging.info('Start Train-Test Split...')
    X_train, X_test, y_train, y_test = train_test_split(
        df[features],
        df[label],
        test_size=appconfig.getfloat('Model','test_size'),
        random_state=0
    )

    # Choose regression model
    logging.info('Start Training...')
    # Option 1: Linear Regression
    model = LinearRegression()

    # Option 2: Random Forest Regressor (uncomment if preferred)
    # model = RandomForestRegressor(
    #     n_estimators=appconfig.getint('Hyperparameters','rf_n_estimators'),
    #     max_depth=appconfig.getint('Hyperparameters','rf_max_depth'),
    #     random_state=0,
    #     n_jobs=appconfig.getint('Hyperparameters','rf_n_jobs')
    # )

    regr = Pipeline(steps=[("preprocessor", preprocessor),
                           ("regression", model)])
    regr.fit(X_train, y_train)

    # Evaluate and Persist
    if evaluation.run(y_test, regr.predict(X_test)):
        logging.info('Persisting model...')
        mdl_meta = {
            'name': appconfig['Model']['name'],
            'metrics': evaluation.get_eval_metrics(y_test, regr.predict(X_test))
        }
        model_registry.register(regr, features, mdl_meta)

    logging.info('Training completed.')
    return None

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    args = argparser.parse_args()
    run(args.data_path)
