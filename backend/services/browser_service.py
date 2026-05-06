import webbrowser
import urllib.parse
import requests
from typing import Dict, Optional


class BrowserService:
    """
    LIAO AI - Ultra Browser Engine (Jarvis Mode)

    Features:
    - Smart website opening
    - Google / YouTube search
    - Direct YouTube play
    - Auto URL detection
    - Internet check
    """

    def __init__(self) -> None:
        self.google_base = "https://www.google.com/search?q="
        self.youtube_search = "https://www.youtube.com/results?search_query="
        self.youtube_watch = "https://www.youtube.com/results?search_query="
        self.default_timeout = 5

        # 🔥 Common sites (fast access)
        self.sites = {
            "youtube": "https://youtube.com",
            "facebook": "https://facebook.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "chatgpt": "https://chat.openai.com",
            "linkedin": "https://linkedin.com",
            "twitter": "https://x.com",
            "instagram": "https://instagram.com",
        }

    # ==================================================
    # 🌐 SMART OPEN (MAIN ENTRY)
    # ==================================================
    def smart_open(self, text: str) -> Dict:
        """
        🔥 Intelligent open handler
        """
        text = text.strip().lower()

        # direct site
        if text in self.sites:
            return self.open_url(self.sites[text], f"{text} opened")

        # youtube special
        if "youtube" in text:
            return self.open_common_site("youtube")

        # looks like domain
        if "." in text and " " not in text:
            return self.open_website(text)

        # fallback → google search
        return self.search_google(text)

    # ==================================================
    # 🔍 SEARCH
    # ==================================================
    def search_google(self, query: str) -> Dict:
        query = query.strip()

        if not query:
            return self._response(False, "Empty query")

        url = self.google_base + urllib.parse.quote_plus(query)
        return self.open_url(url, "Google search opened")

    def search_youtube(self, query: str) -> Dict:
        query = query.strip()

        if not query:
            return self._response(False, "Empty query")

        url = self.youtube_search + urllib.parse.quote_plus(query)
        return self.open_url(url, "YouTube search opened")

    # ==================================================
    # 🎵 DIRECT PLAY (🔥 NEXT LEVEL)
    # ==================================================
    def play_youtube(self, query: str) -> Dict:
        """
        Open YouTube search (auto first video click possible later)
        """
        query = query.strip()

        if not query:
            return self._response(False, "Empty query")

        url = self.youtube_search + urllib.parse.quote_plus(query)

        # 🔥 open search results (fast)
        webbrowser.open(url)

        return self._response(True, "Playing on YouTube", url)

    # ==================================================
    # 🌐 OPEN WEBSITE
    # ==================================================
    def open_website(self, domain: str) -> Dict:
        domain = domain.strip().lower()

        if not domain:
            return self._response(False, "Domain empty")

        if not domain.startswith("http"):
            url = f"https://{domain}"
        else:
            url = domain

        return self.open_url(url, "Website opened")

    def open_common_site(self, name: str) -> Dict:
        key = name.strip().lower()

        if key not in self.sites:
            return self._response(False, "Unknown site")

        return self.open_url(
            self.sites[key],
            f"{name.title()} opened"
        )

    # ==================================================
    # 🔗 CORE URL OPENER
    # ==================================================
    def open_url(self, url: str, message: str = "Opened") -> Dict:
        try:
            webbrowser.open(url)

            return self._response(
                True,
                message,
                url=url
            )

        except Exception as exc:
            return self._response(False, str(exc))

    # ==================================================
    # 🌐 INTERNET CHECK
    # ==================================================
    def check_connection(self) -> Dict:
        try:
            requests.get(
                "https://www.google.com",
                timeout=self.default_timeout
            )

            return self._response(True, "Internet OK")

        except Exception:
            return self._response(False, "No internet")

    # ==================================================
    # 🧠 SMART SEARCH ROUTER
    # ==================================================
    def smart_search(self, text: str) -> Dict:
        """
        🔥 Auto decide Google / YouTube
        """

        text = text.lower()

        if "youtube" in text or "video" in text or "song" in text:
            query = text.replace("youtube", "").replace("video", "")
            return self.search_youtube(query)

        return self.search_google(text)

    # ==================================================
    # RESPONSE FORMAT
    # ==================================================
    def _response(
        self,
        success: bool,
        message: str,
        url: Optional[str] = ""
    ) -> Dict:
        return {
            "success": success,
            "message": message,
            "url": url or ""
        }


# ==================================================
# TEST
# ==================================================
if __name__ == "__main__":
    browser = BrowserService()

    print(browser.smart_open("youtube"))
    print(browser.search_google("fastapi tutorial"))
    print(browser.play_youtube("lofi music"))