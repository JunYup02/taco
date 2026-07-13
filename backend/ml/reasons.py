"""Turn a fitted (StandardScaler + LogisticRegression) pipeline into
human-readable, quantified reason strings for a single prediction.

Contribution of feature i = coef_i * standardized_value_i. Positive
contributions push the prediction toward "scam"; we surface the
highest positive contributors so the explanation always names the
strongest evidence, not just an arbitrary feature list.
"""
from __future__ import annotations


def compute_contributions(pipeline, feature_order: list[str], raw_values: list[float]):
    scaler = pipeline.named_steps["scaler"]
    clf = pipeline.named_steps["clf"]
    standardized = (
        (v - m) / s for v, m, s in zip(raw_values, scaler.mean_, scaler.scale_)
    )
    contributions = [
        coef * z for coef, z in zip(clf.coef_[0], standardized)
    ]
    return list(zip(feature_order, contributions, raw_values))


def top_reasons(pipeline, feature_order, raw_values, templates, top_k=3, min_contribution=0.05):
    contributions = compute_contributions(pipeline, feature_order, raw_values)
    contributions.sort(key=lambda item: item[1], reverse=True)
    reasons = []
    for name, contribution, raw_value in contributions[:top_k]:
        if contribution <= min_contribution:
            continue
        template = templates.get(name)
        if template is None:
            continue
        text = template(raw_value)
        if text:
            reasons.append(text)
    return reasons


LISTING_REASON_TEMPLATES = {
    "price_gap_ratio": lambda v: (
        f"시세 대비 약 {round(v * 100)}% 저렴한 가격" if v >= 0.15 else None
    ),
    "urgency_keyword_count": lambda v: (
        f"긴급성을 강조하는 표현 {int(v)}회 발견 (예: 급처, 오늘까지, 선착순)" if v >= 1 else None
    ),
    "off_platform_keyword_count": lambda v: (
        f"선입금·직거래 불가 등 플랫폼 밖 거래 유도 표현 {int(v)}회 발견" if v >= 1 else None
    ),
    "desc_too_short": lambda v: (
        "상품 설명이 지나치게 짧고 구체적인 정보가 부족함" if v >= 1 else None
    ),
    "excessive_punctuation": lambda v: (
        f"느낌표/물음표 과다 사용 ({int(v)}회) — 자극적인 문체" if v >= 3 else None
    ),
    "stock_photo_reported": lambda v: (
        "제보된 사진이 스톡/타 게시물 재사용 사진으로 의심됨" if v >= 1 else None
    ),
}

SELLER_REASON_TEMPLATES = {
    "account_age_days": lambda v: (
        f"계정 생성 {int(v)}일 이내로 매우 신규 계정" if v <= 30 else None
    ),
    "review_count": lambda v: (
        "거래 후기가 전혀 없음" if v < 1 else (f"거래 후기 {int(v)}건으로 매우 적음" if v < 5 else None)
    ),
    "avg_rating": lambda v: (
        f"평균 평점 {v:.1f}/5.0로 낮음" if 0 < v < 3.5 else None
    ),
    "num_transactions": lambda v: (
        f"거래 이력 {int(v)}건으로 매우 적음" if v < 5 else None
    ),
    "profile_photo_present": lambda v: (
        "프로필 사진 없음" if v < 1 else None
    ),
}
