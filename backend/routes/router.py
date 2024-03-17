from fastapi import APIRouter
from routes.profile_router import profile_router
from routes.date_router import date_router
from routes.page_router import page_router


router = APIRouter(
    responses={404: {"description": "Not found"}}
)

router.include_router(date_router)
router.include_router(page_router)
router.include_router(profile_router)