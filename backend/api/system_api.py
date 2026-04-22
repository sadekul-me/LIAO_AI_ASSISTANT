import os
import platform
import socket
import getpass
import subprocess
from datetime import datetime

from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/system",
    tags=["System"]
)


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def run_command(command: str) -> dict:
    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": process.returncode == 0,
            "output": process.stdout.strip(),
            "error": process.stderr.strip()
        }

    except Exception as exc:
        return {
            "success": False,
            "output": "",
            "error": str(exc)
        }


def current_os() -> str:
    return platform.system().lower()


# --------------------------------------------------
# Health Check
# --------------------------------------------------
@router.get("/")
def system_status():
    return {
        "service": "system",
        "status": "online"
    }


# --------------------------------------------------
# System Info
# --------------------------------------------------
@router.get("/info")
def system_info():
    try:
        return {
            "success": True,
            "hostname": socket.gethostname(),
            "user": getpass.getuser(),
            "platform": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Lock Computer
# --------------------------------------------------
@router.post("/lock")
def lock_pc():
    system = current_os()

    if system == "windows":
        result = run_command(
            "rundll32.exe user32.dll,LockWorkStation"
        )

    elif system == "linux":
        result = run_command(
            "loginctl lock-session"
        )

    else:
        result = {
            "success": False,
            "error": "Unsupported OS."
        }

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "Computer locked."
    }


# --------------------------------------------------
# Shutdown
# --------------------------------------------------
@router.post("/shutdown")
def shutdown_pc():
    system = current_os()

    if system == "windows":
        command = "shutdown /s /t 0"

    elif system == "linux":
        command = "shutdown now"

    else:
        command = ""

    if not command:
        raise HTTPException(
            status_code=400,
            detail="Unsupported OS."
        )

    result = run_command(command)

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "Shutdown command sent."
    }


# --------------------------------------------------
# Restart
# --------------------------------------------------
@router.post("/restart")
def restart_pc():
    system = current_os()

    if system == "windows":
        command = "shutdown /r /t 0"

    elif system == "linux":
        command = "reboot"

    else:
        command = ""

    if not command:
        raise HTTPException(
            status_code=400,
            detail="Unsupported OS."
        )

    result = run_command(command)

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "Restart command sent."
    }


# --------------------------------------------------
# Sleep
# --------------------------------------------------
@router.post("/sleep")
def sleep_pc():
    system = current_os()

    if system == "windows":
        command = (
            "rundll32.exe powrprof.dll,"
            "SetSuspendState 0,1,0"
        )

    elif system == "linux":
        command = "systemctl suspend"

    else:
        command = ""

    if not command:
        raise HTTPException(
            status_code=400,
            detail="Unsupported OS."
        )

    result = run_command(command)

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )

    return {
        "success": True,
        "message": "Sleep command sent."
    }


# --------------------------------------------------
# Current Time
# --------------------------------------------------
@router.get("/time")
def current_time():
    return {
        "success": True,
        "time": datetime.now().strftime(
            "%I:%M:%S %p"
        ),
        "date": datetime.now().strftime(
            "%Y-%m-%d"
        )
    }


# --------------------------------------------------
# Ping Internet
# --------------------------------------------------
@router.get("/ping")
def ping_test():
    host = "8.8.8.8"

    system = current_os()

    command = (
        f"ping -n 1 {host}"
        if system == "windows"
        else f"ping -c 1 {host}"
    )

    result = run_command(command)

    return {
        "success": result["success"],
        "message": (
            "Internet reachable."
            if result["success"]
            else "No response."
        )
    }


# --------------------------------------------------
# Environment Paths
# --------------------------------------------------
@router.get("/paths")
def system_paths():
    return {
        "success": True,
        "cwd": os.getcwd(),
        "home": os.path.expanduser("~"),
        "temp": os.getenv("TEMP", ""),
        "path": os.getenv("PATH", "")
    }