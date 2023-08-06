"""Config file."""
from depht.__main__ import (MIN_CDS_FEATURES, ATT_SENSITIVITY,
                            MIN_LENGTH, MIN_PRODUCTS_NORMAL,
                            MIN_PRODUCTS_STRICT, CPUS, MODEL_DIR, LOCAL_MODELS)
from depht_train.pipelines.train_model import WINDOW

MIN_CDS_FEATURES = MIN_CDS_FEATURES
ATT_SENSITIVITY = ATT_SENSITIVITY

MIN_LENGTH = MIN_LENGTH
MIN_PRODUCTS_NORMAL = MIN_PRODUCTS_NORMAL
MIN_PRODUCTS_STRICT = MIN_PRODUCTS_STRICT

WINDOW = WINDOW
CPUS = CPUS

MODEL_DIR = MODEL_DIR
if not MODEL_DIR.is_dir():
    MODEL_DIR.mkdir(parents=True)

MODEL_URL = "https://osf.io/zt4n3/"

# check that .zip files etc are not added
LOCAL_MODELS = [
    model for model in LOCAL_MODELS if not len(model.split(".")) > 1]
