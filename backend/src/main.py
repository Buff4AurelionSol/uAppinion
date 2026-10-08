from fastapi import FastAPI
from backend.endpoints.api import central_router
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager



from backend.config.db import get_db, Base, engine
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=['*'], 
    allow_headers=['*']
)

app.include_router(central_router)


@app.get("/")
def read_root():
    return {"message": "API de uAppinnion funcionando"}

