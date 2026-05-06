import os
import subprocess
import platform
from pathlib import Path
from typing import Dict, Optional


class AppService:
    """
    LIAO AI - Advanced App & System Control Service (Jarvis Mode)

    Features:
    - Open apps (cross-platform)
    - Run code / scripts
    - Open folders / projects in VS Code
    - System control (shutdown/restart/lock)
    - Shell command execution
    - Smart fallback execution
    """

    def __init__(self) -> None:
        self.system = platform.system().lower()

        self.apps = {
            "chrome": self._chrome_targets(),
            "vscode": self._vscode_targets(),
            "notepad": self._notepad_targets(),
            "calculator": self._calculator_targets(),
            "explorer": self._explorer_targets(),
            "cmd": self._cmd_targets(),
        }

    # ==================================================
    # 🚀 PUBLIC API
    # ==================================================
    def open_app(self, app_name: str) -> Dict[str, object]:
        key = app_name.strip().lower()

        if key not in self.apps:
            return self._result(False, f"Unsupported app: {app_name}")

        for target in self.apps[key]:
            if self._launch(target):
                return self._result(True, f"{app_name} opened", target)

        return self._result(False, f"Failed to open {app_name}")

    def open_path(self, path: str) -> Dict[str, object]:
        target = Path(path).expanduser()

        if not target.exists():
            return self._result(False, "Path not found")

        try:
            if self.system == "windows":
                os.startfile(str(target))
            elif self.system == "darwin":
                subprocess.Popen(["open", str(target)])
            else:
                subprocess.Popen(["xdg-open", str(target)])

            return self._result(True, "Opened path", str(target))

        except Exception as e:
            return self._result(False, str(e))

    # ==================================================
    # 🔥 DEV CONTROL (NEXT LEVEL)
    # ==================================================
    def open_vscode_project(self, path: str) -> Dict[str, object]:
        try:
            subprocess.Popen(["code", path])
            return self._result(True, "VS Code project opened", path)
        except Exception as e:
            return self._result(False, str(e))

    def run_code(self, file_path: str = "main.py") -> Dict[str, object]:
        """
        Auto run Python / JS code
        """
        try:
            if file_path.endswith(".py"):
                subprocess.Popen(["python", file_path])

            elif file_path.endswith(".js"):
                subprocess.Popen(["node", file_path])

            else:
                subprocess.Popen(file_path, shell=True)

            return self._result(True, "Code running", file_path)

        except Exception as e:
            return self._result(False, str(e))

    # ==================================================
    # 🔥 SYSTEM CONTROL
    # ==================================================
    def system_action(self, action: str) -> Dict[str, object]:
        try:
            if self.system == "windows":
                if action == "shutdown":
                    os.system("shutdown /s /t 1")

                elif action == "restart":
                    os.system("shutdown /r /t 1")

                elif action == "lock":
                    os.system("rundll32.exe user32.dll,LockWorkStation")

            elif self.system == "darwin":
                if action == "shutdown":
                    os.system("shutdown -h now")

                elif action == "restart":
                    os.system("shutdown -r now")

            else:
                if action == "shutdown":
                    os.system("shutdown now")

                elif action == "restart":
                    os.system("reboot")

            return self._result(True, f"System action: {action}")

        except Exception as e:
            return self._result(False, str(e))

    # ==================================================
    # 🔥 SHELL EXECUTION (POWER FEATURE)
    # ==================================================
    def run_command(self, command: str) -> Dict[str, object]:
        try:
            subprocess.Popen(command, shell=True)

            return self._result(True, "Command executed", command)

        except Exception as e:
            return self._result(False, str(e))

    # ==================================================
    # 🧠 SMART EXECUTION (AUTO FALLBACK)
    # ==================================================
    def smart_open(self, target: str) -> Dict[str, object]:
        """
        Try everything:
        - app
        - path
        - command
        """
        if target in self.apps:
            return self.open_app(target)

        if Path(target).exists():
            return self.open_path(target)

        return self.run_command(target)

    # ==================================================
    # 📦 INTERNAL LAUNCH
    # ==================================================
    def _launch(self, target: str) -> bool:
        try:
            if self.system == "windows":
                if target.endswith(".exe") and Path(target).exists():
                    subprocess.Popen([target])
                else:
                    subprocess.Popen(target, shell=True)
                return True

            elif self.system == "darwin":
                subprocess.Popen(["open", "-a", target])
                return True

            else:
                subprocess.Popen([target])
                return True

        except Exception:
            return False

    # ==================================================
    # 🎯 APP TARGETS
    # ==================================================
    def _chrome_targets(self):
        if self.system == "windows":
            return [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "start chrome",
            ]
        if self.system == "darwin":
            return ["Google Chrome"]
        return ["google-chrome", "chromium"]

    def _vscode_targets(self):
        if self.system == "windows":
            return [
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                "code",
            ]
        if self.system == "darwin":
            return ["Visual Studio Code"]
        return ["code"]

    def _notepad_targets(self):
        if self.system == "windows":
            return ["notepad"]
        if self.system == "darwin":
            return ["TextEdit"]
        return ["nano", "gedit"]

    def _calculator_targets(self):
        if self.system == "windows":
            return ["calc"]
        if self.system == "darwin":
            return ["Calculator"]
        return ["gnome-calculator"]

    def _explorer_targets(self):
        if self.system == "windows":
            return ["explorer"]
        if self.system == "darwin":
            return ["Finder"]
        return ["xdg-open ."]

    def _cmd_targets(self):
        if self.system == "windows":
            return ["cmd"]
        if self.system == "darwin":
            return ["Terminal"]
        return ["gnome-terminal"]

    # ==================================================
    # 📤 RESPONSE FORMAT
    # ==================================================
    def _result(
        self,
        success: bool,
        message: str,
        target: Optional[str] = None,
    ) -> Dict[str, object]:
        return {
            "success": success,
            "message": message,
            "target": target or "",
        }


# ==================================================
# 🔥 TEST
# ==================================================
if __name__ == "__main__":
    service = AppService()

    print(service.open_app("vscode"))
    print(service.open_vscode_project("."))
    print(service.run_code("test.py"))
    print(service.system_action("lock"))