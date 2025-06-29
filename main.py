import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from infra.config.settings import Settings
from infra.di.Container import Container
from infra.middleware.ExceptionMiddleware import ExceptionMiddleware
from infra.router.routers import routers as v1_routers

container = Container()
config = Settings()

docs_url = '/docs' if config.ENVIRONMENT in ['dev'] else None
root_path = '/dev' if config.ENVIRONMENT in ['dev'] else ''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FastAPI app')

app = FastAPI(docs_url=docs_url, root_path=root_path)

app.container = container

app.include_router(v1_routers)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='Finances APi',
        version='1.0.0',
        description='Gerenciador de finanças',
        routes=app.routes,
    )
    openapi_schema['components']['securitySchemes'] = {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    }
    openapi_schema['security'] = [{'BearerAuth': []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,  # não permite true e allow_origins['*']
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_exception_handler(Exception, ExceptionMiddleware().exception_handler)

add_pagination(app)
