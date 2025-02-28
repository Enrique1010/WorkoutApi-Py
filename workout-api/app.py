from fastapi import FastAPI

from routers import main_router

app = FastAPI()

app.include_router(main_router.main_router_v1, prefix="/api/v1")
