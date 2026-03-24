import base64
import datetime
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from tracker._config import DATABASE
from tracker.models.content import ContentDB, TrackerCreate, ViewDB

TRANSPARENT_PIXEL_GIF = base64.b64decode(
    "R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
)

router = APIRouter(
    prefix="/content",
    tags=["Content"],
)


def _base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")


def _tracker_payload(content: ContentDB, request: Request) -> dict[str, Any]:
    tracking_url = f"{_base_url(request)}/content/{content.id}"
    last_opened_at = content.views[-1].created_at if content.views else None

    return {
        "id": content.id,
        "name": content.name,
        "recipient": content.recipient,
        "subject": content.subject,
        "created_at": content.created_at,
        "open_count": len(content.views),
        "last_opened_at": last_opened_at,
        "tracking_url": tracking_url,
        "email_html": (
            f'<img src="{tracking_url}" alt="" width="1" height="1" '
            'style="display:block;width:1px;height:1px;border:0;" />'
        ),
    }


def _get_content_or_404(content_id: str) -> ContentDB:
    content = DATABASE.search_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return content


@router.get("")
async def get_links(request: Request):
    contents = sorted(
        DATABASE.get_contents().values(),
        key=lambda item: item.created_at,
        reverse=True,
    )
    return [_tracker_payload(content, request) for content in contents]


@router.post("")
async def create_content(payload: TrackerCreate, request: Request):
    content_id = str(uuid4())
    content = ContentDB(
        id=content_id,
        link=content_id,
        name=payload.name.strip(),
        recipient=payload.recipient.strip(),
        subject=payload.subject.strip(),
        created_at=datetime.datetime.now(datetime.timezone.utc),
        user=1,
        views=[],
    )
    if DATABASE.add_content(content):
        return JSONResponse(status_code=201, content=jsonable_encoder(_tracker_payload(content, request)))
    return JSONResponse(status_code=400, content={"message": "Tracker not created"})


@router.delete("/{content_id}")
async def delete_content(content_id: str):
    _get_content_or_404(content_id)
    if DATABASE.delete_content(content_id):
        return {"message": "Tracker deleted"}
    return JSONResponse(status_code=400, content={"message": "Tracker not deleted"})


@router.get("/add")
async def add_content(request: Request):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = TrackerCreate(name=f"Quick tracker {timestamp}")
    return await create_content(payload, request)


@router.get("/{content_id}")
async def get_content(content_id: str, request: Request):
    content = _get_content_or_404(content_id)
    view = ViewDB(
        id=str(uuid4()),
        country=request.client.host if request.client else "unknown",
        ip=request.client.host if request.client else "unknown",
        user_agent=request.headers.get("user-agent", "unknown"),
        created_at=datetime.datetime.now(datetime.timezone.utc),
        request_headers=dict(request.headers.items()),
    )
    DATABASE.add_view_to_content(content.id, view)
    return Response(content=TRANSPARENT_PIXEL_GIF, media_type="image/gif")


@router.get("/{content_id}/detail")
async def get_tracker_detail(content_id: str, request: Request):
    content = _get_content_or_404(content_id)
    payload = _tracker_payload(content, request)
    payload["views"] = jsonable_encoder(content.views)
    return payload


@router.get("/{content_id}/views")
async def get_views(content_id: str):
    content = _get_content_or_404(content_id)
    return jsonable_encoder(content.views)
