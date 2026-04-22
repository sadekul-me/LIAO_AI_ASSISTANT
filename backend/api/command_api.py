from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.app_service import AppService
from backend.services.browser_service import BrowserService
from backend.services.file_service import FileService


router = APIRouter(
    prefix="/command",
    tags=["Command"]
)

app_service = AppService()
browser_service = BrowserService()
file_service = FileService()


# --------------------------------------------------
# Request Models
# --------------------------------------------------
class AppRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)


class UrlRequest(BaseModel):
    url: str = Field(..., min_length=3, max_length=1000)


class FolderRequest(BaseModel):
    path: str = Field(..., min_length=1, max_length=500)


class FileRequest(BaseModel):
    path: str = Field(..., min_length=1, max_length=500)
    content: str = Field(default="")


# --------------------------------------------------
# Health Check
# --------------------------------------------------
@router.get("/")
def command_status():
    return {
        "service": "command",
        "status": "online"
    }


# --------------------------------------------------
# App Controls
# --------------------------------------------------
@router.post("/open-app")
def open_app(request: AppRequest):
    try:
        result = app_service.open_app(request.name)
        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/apps")
def list_apps():
    return {
        "success": True,
        "items": app_service.list_supported_apps()
    }


# --------------------------------------------------
# Browser Controls
# --------------------------------------------------
@router.post("/search")
def search_google(request: SearchRequest):
    try:
        return browser_service.search_google(
            request.query
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.post("/youtube")
def search_youtube(request: SearchRequest):
    try:
        return browser_service.search_youtube(
            request.query
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.post("/open-url")
def open_url(request: UrlRequest):
    try:
        return browser_service.open_url(
            request.url
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# File Controls
# --------------------------------------------------
@router.post("/create-folder")
def create_folder(request: FolderRequest):
    try:
        return file_service.create_folder(
            request.path
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.post("/create-file")
def create_file(request: FileRequest):
    try:
        return file_service.create_file(
            request.path,
            request.content
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/list-files")
def list_files(path: str = "."):
    try:
        return file_service.list_items(path)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Quick Actions
# --------------------------------------------------
@router.post("/quick/{site_name}")
def quick_site(site_name: str):
    try:
        return browser_service.open_common_site(
            site_name
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )