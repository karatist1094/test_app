from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router
from app.api.routers.categories import router as category_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("запуск приложения")
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
app.include_router(category_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["*"],
)

@app.get("/")
def read_base_page():
    return {"hello": "world"}

