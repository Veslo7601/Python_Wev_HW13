from os import environ
import redis.asyncio as redis
from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from My_project.routers import contact, auth
import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = environ.get("REDIS_PORT")

@asynccontextmanager
async def startup(app: FastAPI):
    redis_client = None
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=int(REDIS_PORT),
            db=0,
            encoding="utf-8",
            decode_responses=True
        )
        await redis_client.ping()
        await FastAPILimiter.init(redis_client)
        yield
    except redis.ConnectionError:
        print("Could not connect to Redis. Please check your Redis server.")
        if redis_client:
            await redis_client.close()
        raise
    finally:
        if redis_client:
            await redis_client.close()

app = FastAPI(lifespan=startup)

app.include_router(contact.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
