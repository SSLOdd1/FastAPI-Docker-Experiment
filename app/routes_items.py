from fastapi import APIRouter, Depends
from .deps import get_current_user_dep

router = APIRouter(tags=["items"])


@router.get("/items")
def get_items(current_user=Depends(get_current_user_dep)):
    return {
        "user": current_user.username,
        "items": ["apple", "banana", "carrot"],
    }
