from fastapi import FastAPI
from contextlib import asynccontextmanager

from controllers import auth_controller
from utils import Logger, create_tables

_logger = Logger(logger_name=__name__)._get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield create_tables()
    except Exception as e:
        _logger.error(
            "Database connection cannot be stablised | Error: %s",
            str(e)
        )
        raise f"Error caught on datbase connection: {e}"
    finally:
        print("Database connection stablised")


app = FastAPI(
    title="Greentech Auth API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_controller.auth_router)

@app.get("/", status_code=200, tags=["Health Check"])
async def health_check():
    _logger.info(
        "Health check endpoint called"
    )
    return {"State": "Application running"}