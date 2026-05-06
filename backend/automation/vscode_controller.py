from __future__ import annotations

import subprocess
import time
import platform
import os
from pathlib import Path
from typing import Dict, Optional

try:
    import pyautogui
except ImportError:
    pyautogui = None


class VSCodeController:
    """
    🚀 LIAO AI - VS Code Controller (JARVIS ULTRA v2)

    Features:
    - Smart VS Code launch detection
    - Project-aware execution
    - Auto environment detection (Python venv / Node)
    - Clean subprocess execution (no hacky typing)
    - Optional UI automation
    """

    def __init__(self):
        self.system = platform.system().lower()

    # ==================================================
    # 🔍 CHECK VS CODE RUNNING
    # ==================================================
    def _is_vscode_running(self) -> bool:
        try:
            if self.system == "windows":
                result = subprocess.run(
                    ["tasklist"], capture_output=True, text=True
                )
                return "Code.exe" in result.stdout

            else:
                result = subprocess.run(
                    ["ps", "aux"], capture_output=True, text=True
                )
                return "code" in result.stdout.lower()

        except:
            return False

    # ==================================================
    # 🚀 OPEN VS CODE (SMART)
    # ==================================================
    def open_vscode(self) -> Dict:
        try:
            if not self._is_vscode_running():
                subprocess.Popen(["code"])
                return self._res(True, "VS Code launched")

            return self._res(True, "VS Code already running")

        except Exception as e:
            return self._res(False, str(e))

    def open_project(self, path: str) -> Dict:
        try:
            subprocess.Popen(["code", str(Path(path))])
            return self._res(True, "Project opened", path)

        except Exception as e:
            return self._res(False, str(e))

    def open_file(self, file_path: str) -> Dict:
        try:
            subprocess.Popen(["code", "-r", str(Path(file_path))])
            return self._res(True, "File opened", file_path)

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🧠 PROJECT ROOT DETECTOR
    # ==================================================
    def _detect_project_root(self, file_path: str) -> Path:
        path = Path(file_path).resolve()

        for parent in [path] + list(path.parents):
            if (parent / "package.json").exists() or \
               (parent / "requirements.txt").exists() or \
               (parent / ".git").exists():
                return parent

        return path.parent

    # ==================================================
    # 🔥 ENV DETECTOR
    # ==================================================
    def _detect_env(self, root: Path) -> Dict:
        env = {
            "python": "python",
            "node": "node"
        }

        # Python venv
        venv_path = root / "venv" / "Scripts" / "python.exe"
        if venv_path.exists():
            env["python"] = f'"{venv_path}"'

        # Node (basic)
        if (root / "node_modules").exists():
            env["node"] = "node"

        return env

    # ==================================================
    # 🔥 RUN COMMAND (PROJECT AWARE)
    # ==================================================
    def run_command(self, command: str, cwd: Optional[str] = None) -> Dict:
        try:
            subprocess.Popen(
                command,
                shell=True,
                cwd=cwd or os.getcwd()
            )

            return self._res(True, "Command executed", command)

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🔥 SMART FILE RUNNER (ULTRA)
    # ==================================================
    def run_file(self, file_path: str) -> Dict:

        try:
            file_path = str(Path(file_path).resolve())
            root = self._detect_project_root(file_path)
            env = self._detect_env(root)

            print(f"🚀 ROOT: {root}")

            if file_path.endswith(".py"):
                cmd = f'{env["python"]} "{file_path}"'
                return self.run_command(cmd, cwd=str(root))

            elif file_path.endswith(".js"):
                cmd = f'{env["node"]} "{file_path}"'
                return self.run_command(cmd, cwd=str(root))

            elif file_path.endswith(".ts"):
                cmd = f'npx ts-node "{file_path}"'
                return self.run_command(cmd, cwd=str(root))

            return self.run_command(file_path, cwd=str(root))

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🔥 TERMINAL CONTROL (OPTIONAL)
    # ==================================================
    def open_terminal(self) -> Dict:
        try:
            if not pyautogui:
                return self._res(False, "pyautogui not installed")

            pyautogui.hotkey("ctrl", "`")
            return self._res(True, "Terminal opened")

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🎬 VISUAL EFFECT (OPTIONAL)
    # ==================================================
    def simulate_typing(self, code: str) -> Dict:
        if not pyautogui:
            return self._res(False, "pyautogui not installed")

        pyautogui.click(600, 400)
        time.sleep(0.5)

        pyautogui.write(code, interval=0.01)

        return self._res(True, "Typing simulated")

    # ==================================================
    # 🧠 FULL DEV FLOW
    # ==================================================
    def full_dev_flow(
        self,
        project_path: str,
        file_path: str,
        run: bool = True
    ) -> Dict:

        try:
            self.open_project(project_path)
            time.sleep(2)

            self.open_file(file_path)
            time.sleep(1)

            if run:
                return self.run_file(file_path)

            return self._res(True, "Ready", file_path)

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 📤 RESPONSE
    # ==================================================
    def _res(self, success: bool, message: str, target: Optional[str] = ""):
        return {
            "success": success,
            "message": message,
            "target": target or ""
        }


# ==================================================
# TEST
# ==================================================
if __name__ == "__main__":
    vc = VSCodeController()

    print(vc.open_vscode())
    print(vc.open_project("."))
    print(vc.open_file("test.py"))

    print(vc.run_file("test.py"))