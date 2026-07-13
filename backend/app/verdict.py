LOW_THRESHOLD = 30
HIGH_THRESHOLD = 60


def combine_verdict(listing_probability: float, seller_probability: float):
    listing_score = round(listing_probability * 100, 1)
    seller_score = round(seller_probability * 100, 1)
    combined_score = round((listing_score + seller_score) / 2, 1)

    if combined_score >= HIGH_THRESHOLD:
        risk_level = "high"
        verdict = "위험 - 거래를 권장하지 않습니다"
    elif combined_score >= LOW_THRESHOLD:
        risk_level = "medium"
        verdict = "주의 - 추가 확인이 필요합니다"
    else:
        risk_level = "low"
        verdict = "낮음 - 특이 위험 신호가 적습니다"

    return listing_score, seller_score, combined_score, risk_level, verdict
