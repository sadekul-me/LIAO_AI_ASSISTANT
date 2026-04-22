import os
import subprocess
import platform
from pathlib import Path
from typing import Dict, Optional


class AppService:
    """
    Desktop application launcher service.

    Responsibilities:
    - open common applications
    - open custom executable paths
    - cross-platform basic support
    - structured response output
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

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------
    def open_app(self, app_name: str) -> Dict[str, object]:
        """
        Open predefined application.
        """
        key = app_name.strip().lower()

        if key not in self.apps:
            return self._result(
                success=False,
                message=f"Unsupported application: {app_name}",
            )

        targets = self.apps[key]

        for target in targets:
            if self._launch(target):
                return self._result(
                    success=True,
                    message=f"{app_name} opened successfully.",
                    target=target,
                )

        return self._result(
            success=False,
            message=f"Failed to open {app_name}.",
        )

    def open_path(self, path: str) -> Dict[str, object]:
        """
        Open file or folder path.
        """
        target = Path(path).expanduser()

        if not target.exists():
            return self._result(
                success=False,
                message="Path not found.",
            )

        try:
            if self.system == "windows":
                os.startfile(str(target))

            elif self.system == "darwin":
                subprocess.Popen(["open", str(target)])

            else:
                subprocess.Popen(["xdg-open", str(target)])

            return self._result(
                success=True,
                message="Path opened successfully.",
                target=str(target),
            )

        except Exception as exc:
            return self._result(
                success=False,
                message=str(exc),
            )

    def run_command(self, command: str) -> Dict[str, object]:
        """
        Run shell command.
        """
        try:
            subprocess.Popen(command, shell=True)

            return self._result(
                success=True,
                message="Command executed.",
                target=command,
            )

        except Exception as exc:
            return self._result(
                success=False,
                message=str(exc),
            )

    def available_apps(self) -> list:
        return sorted(self.apps.keys())

    # --------------------------------------------------
    # Launch Logic
    # --------------------------------------------------
    def _launch(self, target: str) -> bool:
        try:
            if self.system == "windows":
                if target.endswith(".exe") and Path(target).exists():
                    subprocess.Popen([target])
                    return True

                subprocess.Popen(target, shell=True)
                return True

            if self.system == "darwin":
                subprocess.Popen(["open", "-a", target])
                return True

            subprocess.Popen([target])
            return True

        except Exception:
            return False

    # --------------------------------------------------
    # App Targets
    # --------------------------------------------------
    def _chrome_targets(self):
        if self.system == "windows":
            return [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "start chrome",
            ]

        if self.system == "darwin":
            return ["Google Chrome"]

        return ["google-chrome", "chrome", "chromium-browser"]

    def _vscode_targets(self):
        if self.system == "windows":
            return [
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
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

        return ["gedit", "nano"]

    def _calculator_targets(self):
        if self.system == "windows":
            return ["calc"]

        if self.system == "darwin":
            return ["Calculator"]

        return ["gnome-calculator", "kcalc"]

    def _explorer_targets(self):
        if self.system == "windows":
            return ["explorer"]

        if self.system == "darwin":
            return ["Finder"]

        return ["nautilus", "xdg-open ."]

    def _cmd_targets(self):
        if self.system == "windows":
            return ["cmd"]

        if self.system == "darwin":
            return ["Terminal"]

        return ["gnome-terminal", "x-terminal-emulator"]

    # --------------------------------------------------
    # Response Format
    # --------------------------------------------------
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


# ------------------------------------------------------
# Local Test
# ------------------------------------------------------
if __name__ == "__main__":
    service = AppService()

    print("Available Apps:", service.available_apps())
    print(service.open_app("chrome"))