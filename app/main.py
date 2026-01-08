from fastapi import FastAPI
from app.api.routes import router
from app.db.models import Base
from app.db.session import engine

app = FastAPI(title="GitHub Repository Tracker")

app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
