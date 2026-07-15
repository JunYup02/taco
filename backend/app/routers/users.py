from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import User, get_session
from app.schemas import WelcomeUserResponse

router = APIRouter()


@router.get("/welcome-user", response_model=WelcomeUserResponse)
def get_welcome_user(session: Session = Depends(get_session)):
    user = session.query(User).order_by(User.id).first()
    if user is None:
        return WelcomeUserResponse(name=None)
    return WelcomeUserResponse(name=user.name)
