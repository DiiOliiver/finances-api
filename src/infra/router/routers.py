from fastapi import APIRouter
from infra.router.endpoint import expenses as expense_router
from infra.router.endpoint import extracts as extracts_router
from infra.router.endpoint import incomes as income_router
from infra.router.endpoint import notebooks as notebook_router
from infra.router.endpoint import users as user_router

routers = APIRouter()

routers.include_router(user_router.router)
routers.include_router(income_router.router)
routers.include_router(notebook_router.router)
routers.include_router(expense_router.router)
routers.include_router(extracts_router.router)
