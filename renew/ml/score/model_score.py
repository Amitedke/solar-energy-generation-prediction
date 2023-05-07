from renew.entity.artifact_entity import RegressionArtifact
from sklearn.metrics import r2_score,mean_squared_error
from renew.logger import logging
from renew.exception import SolarException
import sys

def get_regression_report(y_true,y_pred)->RegressionArtifact:
    try:
        r2 = r2_score(y_true,y_pred)
        rms = mean_squared_error(y_true=y_true,y_pred=y_pred)

        regression_artifact = RegressionArtifact(r2_score=r2,rms=rms)

        return regression_artifact
    except Exception as e:
        raise SolarException(e,sys)