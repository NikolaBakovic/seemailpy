from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["UI"])
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "dashboard.html"


@router.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(TEMPLATE_PATH.read_text(encoding="utf-8"))
