from fastapi import APIRouter
from app.core.option_chain import get_option_chain

router = APIRouter(prefix="/options", tags=["options"])


@router.get("")
def option_chain():
    return get_option_chain()
