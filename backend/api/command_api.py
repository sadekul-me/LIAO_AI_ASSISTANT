from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import traceback

from backend.services.app_service import AppService
from backend.services.browser_service import BrowserService
from backend.services.file_service import FileService
from backend.automation.vscode_controller import VSCodeController
from backend.core.decision_engine import DecisionEngine


router = APIRouter(
    prefix="/command",
    tags=["Command"]
)

# ================================
# SINGLETON SERVICES
# ================================
app_service = AppService()
browser_service = BrowserService()
file_service = FileService()
vscode = VSCodeController()
decision_engine = DecisionEngine()


# ================================
# REQUEST MODEL
# ================================
class CommandRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


# ================================
# HEALTH CHECK
# ================================
@router.get("/")
def status():
    return {
        "service": "command",
        "status": "online",
        "mode": "JARVIS-ULTRA-V5"
    }


# ================================
# 🔥 MAIN EXECUTION ENGINE
# ================================
@router.post("/execute")
def execute_command(request: CommandRequest):

    try:
        raw_text = request.text.strip()
        text = raw_text.lower()

        # ================================
        # BANGLA → ENGLISH NORMALIZER
        # ================================
        bn_map = {
            "খুলো": "open",
            "খুলে": "open",
            "বানাও": "create",
            "তৈরি": "create",
            "লিখ": "write",
            "চালাও": "run",
            "খুঁজ": "search",
            "দেখাও": "open",
            "ভিডিও": "youtube",
            "গান": "music",
        }

        for bn, en in bn_map.items():
            text = text.replace(bn, en)

        # ================================
        # DECISION ENGINE
        # ================================
        decision: Dict[str, Any] = decision_engine.analyze(text)

        intent = decision.get("intent", "chat")
        target = decision.get("target", "")
        action = decision.get("action", "")
        data = decision.get("data", {}) or {}

        print("\n==============================")
        print(f"🔥 INTENT: {intent} | TARGET: {target}")
        print("==============================\n")

        # ================================
        # 💻 DEV ACTIONS
        # ================================

        if intent == "write_code":
            code = data.get("code", "print('🔥 LIAO AI')")

            file_service.write_code(target, code)
            vscode.open_file(target)

            return {
                "success": True,
                "message": "🔥 Code written & opened",
                "file": target
            }

        if intent == "create_file":
            file_service.create_file(target, "")

            try:
                vscode.open_file(target)
            except:
                pass

            return {
                "success": True,
                "message": "📄 File created",
                "file": target
            }

        if intent == "create_folder":
            return file_service.create_folder(target)

        if intent == "create_project":
            project_type = data.get("type", "python")

            res = file_service.create_project(target, project_type)

            try:
                vscode.open_project(target)
            except:
                pass

            return {
                "success": True,
                "message": f"🚀 {project_type} project ready",
                "path": target
            }

        if intent == "run_code":
            return vscode.run_file(target or "main.py")

        # ================================
        # 🖥️ APP CONTROL
        # ================================

        if intent == "open_app":
            return app_service.open_app(target)

        if intent == "open_path":
            return app_service.open_path(target)

        # ================================
        # 🌐 BROWSER CONTROL
        # ================================

        if intent == "search_web":
            return browser_service.search_google(target)

        if intent == "open_website":
            return browser_service.open_website(target)

        if intent == "play_media":
            return browser_service.search_youtube(target)

        if intent == "send_whatsapp":
            return browser_service.open_url(
                f"https://wa.me/?text={target}"
            )

        # ================================
        # ⚙️ SYSTEM
        # ================================

        if intent == "system":
            return app_service.system_action(action)

        # ================================
        # 🧠 FALLBACK
        # ================================
        return {
            "success": True,
            "message": decision.get("message", "Processed"),
            "intent": intent,
            "input": raw_text
        }

    except Exception as e:
        print("❌ COMMAND ERROR:")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Execution failed: {str(e)}"
        )