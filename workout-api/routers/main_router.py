from fastapi import APIRouter

from routers import auth, users, workouts, exercises, misc_routes

main_router_v1 = APIRouter()

main_router_v1.include_router(misc_routes.router, tags=["misc"])
main_router_v1.include_router(auth.router, tags=["auth"])
main_router_v1.include_router(users.router, prefix="/users", tags=["users"])
main_router_v1.include_router(workouts.router, prefix="/workout", tags=["workouts"])
main_router_v1.include_router(exercises.router, prefix="/exercise", tags=["exercises"])
