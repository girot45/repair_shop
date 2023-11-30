from routes.user import router as router_user, current_user

from fastapi import FastAPI, Depends

from database.database import User


app = FastAPI()

app.include_router(router_user)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.fio}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"



