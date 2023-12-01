from fastapi.responses import HTMLResponse

from fastapi import Request, APIRouter

from src.config import templates


router = APIRouter(
    prefix="",
    tags=["Technique"]
)

@router.get("/check-status", response_class=HTMLResponse)
async def check_status(request: Request):
    return templates.TemplateResponse("check_status.html",
                                      {"request": request})

@router.get("/secure/login", response_class=HTMLResponse)
async def check_status(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})