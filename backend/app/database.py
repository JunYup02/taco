import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, String, Float, Boolean, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    DB_PATH = Path(__file__).resolve().parent.parent / "data.db"
    engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=True)


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    listing_title: Mapped[str] = mapped_column(String)
    listing_description: Mapped[str] = mapped_column(String)
    asking_price: Mapped[float] = mapped_column(Float)
    market_price: Mapped[float] = mapped_column(Float, nullable=True)
    stock_photo_reported: Mapped[bool] = mapped_column(Boolean)

    account_age_days: Mapped[float] = mapped_column(Float)
    review_count: Mapped[float] = mapped_column(Float)
    avg_rating: Mapped[float] = mapped_column(Float)
    num_transactions: Mapped[float] = mapped_column(Float)
    profile_photo_present: Mapped[bool] = mapped_column(Boolean)

    listing_score: Mapped[float] = mapped_column(Float)
    seller_score: Mapped[float] = mapped_column(Float)
    combined_score: Mapped[float] = mapped_column(Float)

    is_scam: Mapped[bool] = mapped_column(Boolean)
    notes: Mapped[str] = mapped_column(String, nullable=True)


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
