from fastapi import FastAPI
from .routers import users, excursions, questions
from .internal import admin

app = FastAPI()


@app.get("/", tags=["Index"])
async def root():
    return {"message": "Hello! Good luck to you =)"}


app.include_router(router=admin.router)
app.include_router(router=users.router)
app.include_router(router=excursions.router)
app.include_router(router=questions.router)
