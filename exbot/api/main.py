from fastapi import FastAPI

from api.routers import users, excursions, questions, auth, admin


def init_app():
    app = FastAPI(
        title="Excursion bot", description="This bot for modern art museum", version="1"
    )

    @app.on_event("startup")
    async def startup():
        pass

    @app.on_event("shutdown")
    async def shutdown():
        pass

    return app


app = init_app()


@app.get("/", tags=["Index"])
async def root():
    return {"message": "Hello! Good luck to you =)"}


app.include_router(router=auth.router)
app.include_router(router=admin.router)
app.include_router(router=users.router)
app.include_router(router=excursions.router)
app.include_router(router=questions.router)
