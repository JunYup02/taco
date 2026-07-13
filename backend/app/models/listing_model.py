from pathlib import Path

import joblib

from ml.features import LISTING_FEATURE_ORDER, extract_listing_features
from ml.reasons import LISTING_REASON_TEMPLATES, top_reasons
from app.schemas import ListingInput

ARTIFACT_PATH = Path(__file__).resolve().parent.parent.parent / "ml" / "artifacts" / "listing_model.joblib"
_pipeline = joblib.load(ARTIFACT_PATH)


def score_listing(listing: ListingInput):
    features = extract_listing_features(
        title=listing.title,
        description=listing.description,
        asking_price=listing.asking_price,
        market_price=listing.market_price,
        stock_photo_reported=listing.stock_photo_reported,
    )
    values = [features[name] for name in LISTING_FEATURE_ORDER]
    probability = _pipeline.predict_proba([values])[0][1]
    reasons = top_reasons(_pipeline, LISTING_FEATURE_ORDER, values, LISTING_REASON_TEMPLATES)
    return probability, reasons
