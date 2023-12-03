from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.auth.auth_config import current_user, fastapi_users, \
    auth_backend
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.technique.router import router as tech_router
from src.pages.router import router as pages_router

app = FastAPI()

app.mount("/templates", StaticFiles(directory="src/templates"),
          name="templates")



origins = [
    "http://localhost:8000",
    "http://92.63.176.174:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    if not user.is_admin:
        return {"status": "success", "answer": "Вы не администратор"}
    else:
        return f"Hello, master"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


app.include_router(tech_router)
app.include_router(pages_router)
