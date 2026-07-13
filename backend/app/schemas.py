from typing import Optional

from pydantic import BaseModel, Field


class ListingInput(BaseModel):
    title: str
    description: str
    asking_price: float = Field(gt=0)
    market_price: Optional[float] = Field(default=None, gt=0)
    stock_photo_reported: bool = False


class SellerInput(BaseModel):
    account_age_days: float = Field(ge=0)
    review_count: float = Field(ge=0)
    avg_rating: float = Field(ge=0, le=5, default=0)
    num_transactions: float = Field(ge=0)
    profile_photo_present: bool = True


class AnalyzeRequest(BaseModel):
    listing: ListingInput
    seller: SellerInput


class AnalyzeResponse(BaseModel):
    listing_score: float
    seller_score: float
    combined_score: float
    risk_level: str
    verdict: str
    listing_reasons: list[str]
    seller_reasons: list[str]


class ReportRequest(BaseModel):
    listing: ListingInput
    seller: SellerInput
    is_scam: bool
    notes: Optional[str] = None


class ReportResponse(BaseModel):
    id: int
    message: str
