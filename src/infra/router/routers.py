from fastapi import APIRouter

from infra.router.endpoint import incomes as income_router
from infra.router.endpoint import users as user_router

routers = APIRouter()

routers.include_router(user_router.router)
routers.include_router(income_router.router)
