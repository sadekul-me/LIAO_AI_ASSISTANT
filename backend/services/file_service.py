from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from backend.automation.vscode_controller import VSCodeController


class FileService:
    """
    🚀 LIAO AI - File Engine (JARVIS ULTRA v2)

    Features:
    - Smart file + folder control
    - Auto open in VS Code
    - AI-ready code writing
    - Project scaffolding
    - Safe delete system
    - Multi-file generation
    - Dev workflow integration
    """

    def __init__(self, base_path: Optional[str] = None) -> None:
        self.base_path = Path(base_path).resolve() if base_path else Path.cwd()
        self.vscode = VSCodeController()

        self.protected = ["C:\\Windows", "/System", "/usr"]

    # ==================================================
    # 🔥 CORE: CREATE + OPEN
    # ==================================================
    def create_and_open(self, file_path: str, content: str = "") -> Dict:
        path = self._resolve(file_path)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            # overwrite safely
            path.write_text(content, encoding="utf-8")

            self.vscode.open_file(str(path))

            return self._res(True, "File created & opened", str(path))

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🧠 SMART WRITE
    # ==================================================
    def write_code(
        self,
        file_path: str,
        code: str,
        mode: str = "overwrite",  # overwrite | append
        run: bool = False
    ) -> Dict:

        path = self._resolve(file_path)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            if mode == "append" and path.exists():
                with open(path, "a", encoding="utf-8") as f:
                    f.write("\n" + code)
            else:
                path.write_text(code, encoding="utf-8")

            # open in VS Code
            self.vscode.open_file(str(path))

            # optional run
            if run:
                self.vscode.run_file(str(path))

            return self._res(True, "Code written", str(path))

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 📁 FOLDER
    # ==================================================
    def create_folder(self, folder_path: str) -> Dict:
        path = self._resolve(folder_path)

        try:
            path.mkdir(parents=True, exist_ok=True)
            return self._res(True, "Folder created", str(path))

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🚀 PROJECT GENERATOR
    # ==================================================
    def create_project(self, name: str, type_: str = "python") -> Dict:
        root = self._resolve(name)

        try:
            root.mkdir(parents=True, exist_ok=True)

            if type_ == "python":
                self._python_project(root)

            elif type_ == "react":
                self._react_project(root)

            elif type_ == "node":
                self._node_project(root)

            # open project
            self.vscode.open_project(str(root))

            return self._res(True, f"{type_} project ready", str(root))

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🧠 PROJECT TEMPLATES
    # ==================================================
    def _python_project(self, root: Path):
        (root / "main.py").write_text(
            "def main():\n    print('🔥 LIAO AI Running')\n\nif __name__=='__main__': main()",
            encoding="utf-8"
        )

        (root / "requirements.txt").write_text("", encoding="utf-8")

    def _react_project(self, root: Path):
        (root / "src").mkdir(exist_ok=True)
        (root / "public").mkdir(exist_ok=True)

        (root / "src" / "App.jsx").write_text(
            "export default function App(){return <h1>🔥 LIAO AI</h1>}",
            encoding="utf-8"
        )

    def _node_project(self, root: Path):
        (root / "index.js").write_text(
            "console.log('🔥 LIAO Node App');",
            encoding="utf-8"
        )

        (root / "package.json").write_text(
            '{ "name": "liao-app", "version": "1.0.0" }',
            encoding="utf-8"
        )

    # ==================================================
    # 📖 READ
    # ==================================================
    def read_file(self, file_path: str) -> Dict:
        path = self._resolve(file_path)

        try:
            if not path.exists():
                return self._res(False, "Not found")

            return {
                "success": True,
                "content": path.read_text(encoding="utf-8"),
                "path": str(path),
            }

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # ✏️ RENAME
    # ==================================================
    def rename(self, source: str, new_name: str) -> Dict:
        path = self._resolve(source)

        try:
            target = path.parent / new_name
            path.rename(target)

            return self._res(True, "Renamed", str(target))

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🗑️ DELETE (SAFE)
    # ==================================================
    def delete(self, target_path: str) -> Dict:
        path = self._resolve(target_path)

        if any(str(path).startswith(p) for p in self.protected):
            return self._res(False, "Protected path!")

        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

            return self._res(True, "Deleted", str(path))

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 📦 COPY / MOVE
    # ==================================================
    def copy(self, src: str, dst: str) -> Dict:
        s = self._resolve(src)
        d = self._resolve(dst)

        try:
            if s.is_dir():
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(s, d)

            return self._res(True, "Copied", str(d))

        except Exception as e:
            return self._res(False, str(e))

    def move(self, src: str, dst: str) -> Dict:
        try:
            shutil.move(str(self._resolve(src)), str(self._resolve(dst)))
            return self._res(True, "Moved", dst)

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 📂 LIST
    # ==================================================
    def list_items(self, folder: str = ".") -> Dict:
        path = self._resolve(folder)

        try:
            items = []

            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "folder" if item.is_dir() else "file",
                    "modified": datetime.fromtimestamp(
                        item.stat().st_mtime
                    ).strftime("%Y-%m-%d %H:%M")
                })

            return {
                "success": True,
                "items": items,
                "path": str(path)
            }

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # 🔥 MULTI FILE (AI READY)
    # ==================================================
    def create_multiple_files(self, files: Dict[str, str]) -> Dict:
        try:
            for path, content in files.items():
                self.write_code(path, content)

            return self._res(True, "Multiple files created")

        except Exception as e:
            return self._res(False, str(e))

    # ==================================================
    # HELPERS
    # ==================================================
    def _resolve(self, path: str) -> Path:
        p = Path(path)
        return p if p.is_absolute() else (self.base_path / p).resolve()

    def _res(self, success: bool, message: str, path: str = "") -> Dict:
        return {
            "success": success,
            "message": message,
            "path": path
        }


# ==================================================
# TEST
# ==================================================
if __name__ == "__main__":
    fs = FileService()

    print(fs.create_project("liao_project", "python"))

    print(
        fs.write_code(
            "liao_project/test.py",
            "print('🔥 Jarvis Level AI')",
            run=True
        )
    )