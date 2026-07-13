from fastapi import APIRouter

from app.models.listing_model import score_listing
from app.models.seller_model import score_seller
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.verdict import combine_verdict

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    listing_probability, listing_reasons = score_listing(request.listing)
    seller_probability, seller_reasons = score_seller(request.seller)
    listing_score, seller_score, combined_score, risk_level, verdict = combine_verdict(
        listing_probability, seller_probability
    )

    return AnalyzeResponse(
        listing_score=listing_score,
        seller_score=seller_score,
        combined_score=combined_score,
        risk_level=risk_level,
        verdict=verdict,
        listing_reasons=listing_reasons,
        seller_reasons=seller_reasons,
    )
