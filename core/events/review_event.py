from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from utils.time import utc_now_iso


#ENUM TYPES FOR REVIEW EVENTS
class ReviewEventTypes(str, Enum):
    REVIEW_CREATE_SUCCESS = "reviews.create_review"


# BASE MODEL FOR REVIEW EVENT
class BaseReviewEvent(BaseModel):
    event_type: ReviewEventTypes
    rating: float


# EVENT BUILDER FUNCTION

def build_story_create_success_event(rating: float) -> dict:
    return BaseReviewEvent(
        event_type=ReviewEventTypes.REVIEW_CREATE_SUCCESS,
        rating= rating
    ).model_dump()


