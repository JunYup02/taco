from pathlib import Path

import joblib

from ml.features import SELLER_FEATURE_ORDER, extract_seller_features
from ml.reasons import SELLER_REASON_TEMPLATES, top_reasons
from app.schemas import SellerInput

ARTIFACT_PATH = Path(__file__).resolve().parent.parent.parent / "ml" / "artifacts" / "seller_model.joblib"
_pipeline = joblib.load(ARTIFACT_PATH)


def score_seller(seller: SellerInput):
    features = extract_seller_features(
        account_age_days=seller.account_age_days,
        review_count=seller.review_count,
        avg_rating=seller.avg_rating,
        num_transactions=seller.num_transactions,
        profile_photo_present=seller.profile_photo_present,
    )
    values = [features[name] for name in SELLER_FEATURE_ORDER]
    probability = _pipeline.predict_proba([values])[0][1]
    reasons = top_reasons(_pipeline, SELLER_FEATURE_ORDER, values, SELLER_REASON_TEMPLATES)
    return probability, reasons
