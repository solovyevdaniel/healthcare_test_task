from fastapi import APIRouter

from api.endpoints import messages

api_router = APIRouter(prefix='/api')
api_router.include_router(messages.router)
