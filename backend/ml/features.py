"""Interpretable feature extraction shared by training scripts and the live API.

Every feature here is deliberately hand-engineered (not a TF-IDF bag-of-words)
so that a trained model's coefficients can be turned into human-readable
"why" strings for the combined verdict.
"""
from __future__ import annotations

import re

URGENCY_KEYWORDS = [
    "오늘까지", "지금 바로", "지금바로", "빨리", "급처", "급매", "마감임박",
    "한정수량", "선착순", "서두르세요", "곧 마감", "당일", "즉시",
    "urgent", "hurry", "today only", "act now", "limited time",
]

OFF_PLATFORM_KEYWORDS = [
    "선입금", "계좌이체", "무통장", "직거래 불가", "안전거래 거부", "카톡으로",
    "문자로 연락", "카카오톡", "라인으로", "텔레그램", "개인 계좌",
    "wire transfer", "western union", "gift card", "venmo only", "cashapp",
]


def _count_keywords(text: str, keywords: list[str]) -> int:
    text_lower = text.lower()
    return sum(text_lower.count(kw.lower()) for kw in keywords)


def extract_listing_features(
    title: str,
    description: str,
    asking_price: float,
    market_price: float | None,
    stock_photo_reported: bool,
) -> dict[str, float]:
    full_text = f"{title}\n{description}"
    word_count = len(description.split())

    if market_price and market_price > 0:
        price_gap_ratio = max(0.0, (market_price - asking_price) / market_price)
        price_gap_ratio = min(price_gap_ratio, 1.0)
    else:
        price_gap_ratio = 0.0

    return {
        "price_gap_ratio": price_gap_ratio,
        "urgency_keyword_count": float(_count_keywords(full_text, URGENCY_KEYWORDS)),
        "off_platform_keyword_count": float(_count_keywords(full_text, OFF_PLATFORM_KEYWORDS)),
        "desc_too_short": 1.0 if word_count < 15 else 0.0,
        "excessive_punctuation": float(len(re.findall(r"[!?]", full_text))),
        "stock_photo_reported": 1.0 if stock_photo_reported else 0.0,
    }


LISTING_FEATURE_ORDER = [
    "price_gap_ratio",
    "urgency_keyword_count",
    "off_platform_keyword_count",
    "desc_too_short",
    "excessive_punctuation",
    "stock_photo_reported",
]


def extract_seller_features(
    account_age_days: float,
    review_count: float,
    avg_rating: float,
    num_transactions: float,
    profile_photo_present: bool,
) -> dict[str, float]:
    return {
        "account_age_days": float(account_age_days),
        "review_count": float(review_count),
        "avg_rating": float(avg_rating),
        "num_transactions": float(num_transactions),
        "profile_photo_present": 1.0 if profile_photo_present else 0.0,
    }


SELLER_FEATURE_ORDER = [
    "account_age_days",
    "review_count",
    "avg_rating",
    "num_transactions",
    "profile_photo_present",
]
