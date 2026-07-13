"""Synthetic labeled datasets used to train the listing and seller models.

There is no real labeled fraud dataset available for v1, so we simulate one:
draw a class label, then sample each feature from a class-conditional
distribution with deliberate overlap between classes so the resulting
classifier is imperfect and probabilistic, like a real-world model would be.
"""
from __future__ import annotations

import numpy as np

from ml.features import LISTING_FEATURE_ORDER, SELLER_FEATURE_ORDER


def generate_listing_dataset(n: int = 3000, seed: int = 42):
    rng = np.random.default_rng(seed)
    is_scam = rng.random(n) < 0.4

    n_scam = int(is_scam.sum())
    n_legit = n - n_scam

    price_gap_ratio = np.empty(n)
    price_gap_ratio[is_scam] = np.clip(rng.normal(0.45, 0.2, n_scam), 0, 1)
    price_gap_ratio[~is_scam] = np.clip(rng.normal(0.05, 0.1, n_legit), 0, 1)

    urgency_keyword_count = np.empty(n)
    urgency_keyword_count[is_scam] = rng.poisson(2.5, n_scam)
    urgency_keyword_count[~is_scam] = rng.poisson(0.3, n_legit)

    off_platform_keyword_count = np.empty(n)
    off_platform_keyword_count[is_scam] = rng.poisson(1.8, n_scam)
    off_platform_keyword_count[~is_scam] = rng.poisson(0.2, n_legit)

    desc_too_short = np.empty(n)
    desc_too_short[is_scam] = rng.random(n_scam) < 0.55
    desc_too_short[~is_scam] = rng.random(n_legit) < 0.15

    excessive_punctuation = np.empty(n)
    excessive_punctuation[is_scam] = rng.poisson(1.5, n_scam)
    excessive_punctuation[~is_scam] = rng.poisson(0.3, n_legit)

    stock_photo_reported = np.empty(n)
    stock_photo_reported[is_scam] = rng.random(n_scam) < 0.35
    stock_photo_reported[~is_scam] = rng.random(n_legit) < 0.05

    X = np.column_stack([
        price_gap_ratio,
        urgency_keyword_count,
        off_platform_keyword_count,
        desc_too_short,
        excessive_punctuation,
        stock_photo_reported,
    ])
    assert list(LISTING_FEATURE_ORDER) == [
        "price_gap_ratio", "urgency_keyword_count", "off_platform_keyword_count",
        "desc_too_short", "excessive_punctuation", "stock_photo_reported",
    ]
    y = is_scam.astype(int)
    return X, y


def generate_seller_dataset(n: int = 3000, seed: int = 43):
    rng = np.random.default_rng(seed)
    is_scam = rng.random(n) < 0.4

    n_scam = int(is_scam.sum())
    n_legit = n - n_scam

    account_age_days = np.empty(n)
    account_age_days[is_scam] = np.clip(rng.normal(15, 25, n_scam), 0, 3000)
    account_age_days[~is_scam] = np.clip(rng.normal(500, 350, n_legit), 0, 3000)

    review_count = np.empty(n)
    review_count[is_scam] = np.clip(rng.normal(2, 4, n_scam), 0, None)
    review_count[~is_scam] = np.clip(rng.normal(40, 30, n_legit), 0, None)

    avg_rating = np.empty(n)
    avg_rating[is_scam] = np.clip(rng.normal(3.0, 1.5, n_scam), 0, 5)
    avg_rating[~is_scam] = np.clip(rng.normal(4.6, 0.3, n_legit), 0, 5)
    avg_rating[review_count < 1] = 0.0

    num_transactions = np.empty(n)
    num_transactions[is_scam] = np.clip(rng.normal(3, 5, n_scam), 0, None)
    num_transactions[~is_scam] = np.clip(rng.normal(60, 40, n_legit), 0, None)

    profile_photo_present = np.empty(n)
    profile_photo_present[is_scam] = rng.random(n_scam) < 0.4
    profile_photo_present[~is_scam] = rng.random(n_legit) < 0.9

    X = np.column_stack([
        account_age_days,
        review_count,
        avg_rating,
        num_transactions,
        profile_photo_present,
    ])
    assert list(SELLER_FEATURE_ORDER) == [
        "account_age_days", "review_count", "avg_rating",
        "num_transactions", "profile_photo_present",
    ]
    y = is_scam.astype(int)
    return X, y
