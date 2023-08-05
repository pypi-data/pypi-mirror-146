from . import models
from .api.client import Client
from .vectice import Vectice, create_run, save_after_run, save_job

_AUTOLOGGING = []

try:
    import mlflow.sklearn as sklearn
    import mlflow.tracking.fluent.autolog as autolog

    _AUTOLOGGING = ["autolog", "sklearn"]

except ImportError:
    pass


__all__ = ["Vectice", "create_run", "save_after_run", "save_job", "Client", "models"] + _AUTOLOGGING
