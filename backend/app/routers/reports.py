from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import Report, get_session
from app.models.listing_model import score_listing
from app.models.seller_model import score_seller
from app.schemas import ReportRequest, ReportResponse
from app.verdict import combine_verdict

router = APIRouter()


@router.post("/reports", response_model=ReportResponse)
def create_report(request: ReportRequest, session: Session = Depends(get_session)):
    listing_probability, _ = score_listing(request.listing)
    seller_probability, _ = score_seller(request.seller)
    listing_score, seller_score, combined_score, _, _ = combine_verdict(
        listing_probability, seller_probability
    )

    report = Report(
        listing_title=request.listing.title,
        listing_description=request.listing.description,
        asking_price=request.listing.asking_price,
        market_price=request.listing.market_price,
        stock_photo_reported=request.listing.stock_photo_reported,
        account_age_days=request.seller.account_age_days,
        review_count=request.seller.review_count,
        avg_rating=request.seller.avg_rating,
        num_transactions=request.seller.num_transactions,
        profile_photo_present=request.seller.profile_photo_present,
        listing_score=listing_score,
        seller_score=seller_score,
        combined_score=combined_score,
        is_scam=request.is_scam,
        notes=request.notes,
    )
    session.add(report)
    session.commit()
    session.refresh(report)

    return ReportResponse(id=report.id, message="신고가 접수되었습니다. 모델 개선에 활용됩니다.")
