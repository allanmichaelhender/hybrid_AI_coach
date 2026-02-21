from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.api import api_router
from core.config import settings
from auth import router as auth_router
from schemas import user
from deps import get_current_user


def get_application() -> FastAPI:
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,  # Required for JWT headers
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(
        auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"]
    )

    _app.include_router(api_router, prefix=settings.API_V1_STR)

    return _app


app = get_application()


@app.get("/")
def root():
    return {"message": "Server is running"}


@app.get("/users/me", response_model=user.UserOut)
def read_user_me(current_user: user.UserOut = Depends(get_current_user)):
    return current_user
