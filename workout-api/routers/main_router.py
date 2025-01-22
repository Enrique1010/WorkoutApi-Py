from fastapi import APIRouter

from routers import auth, users, workouts, exercises

main_router_v1 = APIRouter()

main_router_v1.include_router(auth.router, tags=["auth"])
main_router_v1.include_router(users.router, tags=["users"])
main_router_v1.include_router(workouts.router, prefix="/workout", tags=["workouts"])
main_router_v1.include_router(exercises.router, prefix="/exercise", tags=["exercises"])
