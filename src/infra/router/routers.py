from fastapi import APIRouter

from infra.router.endpoint import users as user_router

routers = APIRouter()

routers.include_router(user_router.router)
