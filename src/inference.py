# """
# This module encapsulates model inference.
# """

# from joblib import dump, load
# import pandas as pd
# import numpy as np
# from src.data_processor import preprocess
# from src.model_registry import retrieve
# from src.config import appconfig

# def get_prediction(**kwargs):
#     """
#     Get prediction for given data.
#         Parameters:
#             kwargs: Keyworded argument list containing the data for prediction
#         Returns:
#             Predicted class in str
#     """
#     clf, features = retrieve(appconfig['Model']['name'])
#     pred_df = pd.DataFrame(kwargs, index=[0])
#     pred_df = preprocess(pred_df)
#     pred = clf.predict(pred_df[features])
#     return pred[0]


"""
This module encapsulates model inference for HDB rent prediction.
"""

import pandas as pd
from src.data_processor import preprocess   # your HDB-specific preprocessing
from src.model_registry import retrieve
from src.config import appconfig

def get_prediction(**kwargs):
    """
    Get rent prediction for given flat details.
        Parameters:
            kwargs: Keyword arguments containing flat details
        Returns:
            Predicted monthly rent (float)
    """
    # Load model and features
    clf, features = retrieve(appconfig['Model']['name'])

    # Build dataframe from inputs
    pred_df = pd.DataFrame([kwargs])

    # Apply HDB preprocessing (year/month extraction, text normalization)
    pred_df = preprocess(pred_df)

    # Predict rent
    pred = clf.predict(pred_df[features])
    return float(pred[0])
