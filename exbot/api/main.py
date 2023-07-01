import fastapi
from fastapi import FastAPI, Depends, security
from .routers import users, excursions, questions
from .internal import admin
from database import services

app = FastAPI()

# services.create_database()


@app.get("/", tags=["Index"])
async def root():
    return {"message": "Hello! Happy birthday! Good luck to you)"}


app.include_router(router=admin.router)
app.include_router(router=users.router)
app.include_router(router=excursions.router)
app.include_router(router=questions.router)
