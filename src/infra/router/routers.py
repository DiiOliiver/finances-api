from fastapi import APIRouter

from infra.router.endpoint.users import router as user_router

routers = APIRouter()

routers.include_router(user_router)
