import os
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------
class RepoRequest(BaseModel):
    path: str = Field(..., min_length=1, max_length=500)


class InitRequest(BaseModel):
    path: str = Field(..., min_length=1, max_length=500)
    remote_url: Optional[str] = Field(default="")


class CommitRequest(BaseModel):
    path: str = Field(..., min_length=1, max_length=500)
    message: str = Field(..., min_length=1, max_length=300)


class CloneRequest(BaseModel):
    repo_url: str = Field(..., min_length=5, max_length=1000)
    destination: Optional[str] = Field(default="")


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def run_git_command(
    repo_path: str,
    args: list[str]
) -> dict:

    try:
        process = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            capture_output=True,
            text=True,
            shell=True
        )

        output = process.stdout.strip()
        error = process.stderr.strip()

        return {
            "success": process.returncode == 0,
            "output": output,
            "error": error
        }

    except Exception as exc:
        return {
            "success": False,
            "output": "",
            "error": str(exc)
        }


def ensure_folder(path: str):
    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------
@router.get("/")
def github_status():
    return {
        "service": "github",
        "status": "online"
    }


# --------------------------------------------------
# Git Init
# --------------------------------------------------
@router.post("/init")
def git_init(request: InitRequest):
    ensure_folder(request.path)

    result = run_git_command(
        request.path,
        ["init"]
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    if request.remote_url:
        run_git_command(
            request.path,
            [
                "remote",
                "add",
                "origin",
                request.remote_url
            ]
        )

    return {
        "success": True,
        "message": "Repository initialized."
    }


# --------------------------------------------------
# Git Status
# --------------------------------------------------
@router.post("/status")
def git_status(request: RepoRequest):
    result = run_git_command(
        request.path,
        ["status"]
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return result


# --------------------------------------------------
# Git Add All
# --------------------------------------------------
@router.post("/add")
def git_add(request: RepoRequest):
    result = run_git_command(
        request.path,
        ["add", "."]
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "All files staged."
    }


# --------------------------------------------------
# Git Commit
# --------------------------------------------------
@router.post("/commit")
def git_commit(request: CommitRequest):
    result = run_git_command(
        request.path,
        ["commit", "-m", request.message]
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "Commit created.",
        "output": result["output"]
    }


# --------------------------------------------------
# Git Push
# --------------------------------------------------
@router.post("/push")
def git_push(request: RepoRequest):
    result = run_git_command(
        request.path,
        ["push", "-u", "origin", "main"]
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "Push completed.",
        "output": result["output"]
    }


# --------------------------------------------------
# Git Pull
# --------------------------------------------------
@router.post("/pull")
def git_pull(request: RepoRequest):
    result = run_git_command(
        request.path,
        ["pull"]
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "Pull completed.",
        "output": result["output"]
    }


# --------------------------------------------------
# Clone Repository
# --------------------------------------------------
@router.post("/clone")
def git_clone(request: CloneRequest):
    destination = request.destination.strip()

    try:
        args = ["git", "clone", request.repo_url]

        if destination:
            args.append(destination)

        process = subprocess.run(
            args,
            capture_output=True,
            text=True,
            shell=True
        )

        if process.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=process.stderr.strip()
            )

        return {
            "success": True,
            "message": "Repository cloned."
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Remote List
# --------------------------------------------------
@router.post("/remote")
def git_remote(request: RepoRequest):
    result = run_git_command(
        request.path,
        ["remote", "-v"]
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return result