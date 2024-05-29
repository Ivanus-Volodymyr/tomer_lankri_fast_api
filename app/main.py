import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.routers import auth_router, posts_router

app = FastAPI(
    title="Back End",
    description="""
    Back End - Test task
    """,)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["healthcheck"])
async def health_check():
    result = {"healthcheck": 200}
    return result


app.include_router(auth_router.router)
app.include_router(posts_router.router)
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True
    )
