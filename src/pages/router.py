from fastapi.responses import HTMLResponse

from fastapi import Request, APIRouter, Depends, HTTPException

from src.auth.auth_config import current_user
from src.auth.models import User
from src.config import templates


router = APIRouter(
    prefix="",
    tags=["Pages"]
)

@router.get("/check-status", response_class=HTMLResponse)
async def check_status(request: Request):
    return templates.TemplateResponse("check_status.html",
                                      {"request": request})

@router.get("/secure/login", response_class=HTMLResponse)
async def secure_login(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})

@router.get("/secure/register", response_class=HTMLResponse)
async def secure_register(
        request: Request,
        user: User = Depends(current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=302, detail="Redirecting...",
                            headers={"Location": "/check-status"})

    return templates.TemplateResponse("register.html",
                                      {"request": request})