import pandas as pd
from sklearn.model_selection import cross_val_predict
from .model_validator import CustomTsCv

def predict_on_cv(model,
                  features: pd.DataFrame,
                  targets: pd.DataFrame,
                  cv: CustomTsCv):
    """
      - it is to fit and predict the model on all cv test section
      - returns prediction for ALL features
      - input cv needs to make all datapoint one time and only one time as a test
        - otherwise exception: "cross_val_predict only works for partitions TimeSeriesSplit"
    """
    assert cv.train_shuffle_block_size is None, "predict results distorted when shuffle indexes on split"
    result = cross_val_predict(model, features, targets, cv=cv)

    return result