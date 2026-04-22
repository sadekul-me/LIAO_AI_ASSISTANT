import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class FileService:
    """
    File system utility service.

    Features:
    - create files
    - create folders
    - read files
    - write files
    - append files
    - rename
    - delete
    - copy / move
    - list directory items
    """

    def __init__(self, base_path: Optional[str] = None) -> None:
        self.base_path = Path(base_path).resolve() if base_path else Path.cwd()

    # --------------------------------------------------
    # Create
    # --------------------------------------------------
    def create_file(
        self,
        file_path: str,
        content: str = ""
    ) -> Dict[str, object]:

        path = self._resolve(file_path)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

            return self._response(
                True,
                "File created successfully.",
                str(path)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    def create_folder(
        self,
        folder_path: str
    ) -> Dict[str, object]:

        path = self._resolve(folder_path)

        try:
            path.mkdir(parents=True, exist_ok=True)

            return self._response(
                True,
                "Folder created successfully.",
                str(path)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    # --------------------------------------------------
    # Read / Write
    # --------------------------------------------------
    def read_file(
        self,
        file_path: str
    ) -> Dict[str, object]:

        path = self._resolve(file_path)

        try:
            if not path.exists():
                return self._response(False, "File not found.")

            content = path.read_text(encoding="utf-8")

            return {
                "success": True,
                "message": "File read successfully.",
                "path": str(path),
                "content": content
            }

        except Exception as exc:
            return self._response(False, str(exc))

    def write_file(
        self,
        file_path: str,
        content: str
    ) -> Dict[str, object]:

        path = self._resolve(file_path)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

            return self._response(
                True,
                "File updated successfully.",
                str(path)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    def append_file(
        self,
        file_path: str,
        content: str
    ) -> Dict[str, object]:

        path = self._resolve(file_path)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "a", encoding="utf-8") as file:
                file.write(content)

            return self._response(
                True,
                "Content appended successfully.",
                str(path)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    # --------------------------------------------------
    # Rename / Delete
    # --------------------------------------------------
    def rename(
        self,
        source: str,
        new_name: str
    ) -> Dict[str, object]:

        path = self._resolve(source)

        try:
            if not path.exists():
                return self._response(False, "Source not found.")

            target = path.parent / new_name
            path.rename(target)

            return self._response(
                True,
                "Renamed successfully.",
                str(target)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    def delete(
        self,
        target_path: str
    ) -> Dict[str, object]:

        path = self._resolve(target_path)

        try:
            if not path.exists():
                return self._response(False, "Path not found.")

            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

            return self._response(
                True,
                "Deleted successfully.",
                str(path)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    # --------------------------------------------------
    # Copy / Move
    # --------------------------------------------------
    def copy(
        self,
        source: str,
        destination: str
    ) -> Dict[str, object]:

        src = self._resolve(source)
        dst = self._resolve(destination)

        try:
            if not src.exists():
                return self._response(False, "Source not found.")

            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

            return self._response(
                True,
                "Copied successfully.",
                str(dst)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    def move(
        self,
        source: str,
        destination: str
    ) -> Dict[str, object]:

        src = self._resolve(source)
        dst = self._resolve(destination)

        try:
            if not src.exists():
                return self._response(False, "Source not found.")

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))

            return self._response(
                True,
                "Moved successfully.",
                str(dst)
            )

        except Exception as exc:
            return self._response(False, str(exc))

    # --------------------------------------------------
    # Directory Listing
    # --------------------------------------------------
    def list_items(
        self,
        folder_path: str = "."
    ) -> Dict[str, object]:

        path = self._resolve(folder_path)

        try:
            if not path.exists():
                return self._response(False, "Folder not found.")

            items: List[dict] = []

            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "folder" if item.is_dir() else "file",
                    "modified": datetime.fromtimestamp(
                        item.stat().st_mtime
                    ).strftime("%Y-%m-%d %H:%M:%S")
                })

            return {
                "success": True,
                "message": "Items loaded.",
                "path": str(path),
                "items": items
            }

        except Exception as exc:
            return self._response(False, str(exc))

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def exists(self, target_path: str) -> bool:
        return self._resolve(target_path).exists()

    def _resolve(self, path: str) -> Path:
        target = Path(path)

        if target.is_absolute():
            return target.resolve()

        return (self.base_path / target).resolve()

    def _response(
        self,
        success: bool,
        message: str,
        path: str = ""
    ) -> Dict[str, object]:
        return {
            "success": success,
            "message": message,
            "path": path
        }


# --------------------------------------------------
# Local Test
# --------------------------------------------------
if __name__ == "__main__":
    fs = FileService()

    print(fs.create_folder("demo"))
    print(fs.create_file("demo/test.txt", "Hello LIAO"))
    print(fs.read_file("demo/test.txt"))
    print(fs.list_items("demo"))