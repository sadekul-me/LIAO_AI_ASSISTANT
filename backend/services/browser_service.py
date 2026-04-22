import webbrowser
import urllib.parse
import requests
from typing import Dict, Optional


class BrowserService:
    """
    Browser and web utility service.

    Features:
    - open websites
    - Google search
    - YouTube search
    - open direct URLs
    - check internet status
    """

    def __init__(self) -> None:
        self.google_base = "https://www.google.com/search?q="
        self.youtube_base = "https://www.youtube.com/results?search_query="
        self.default_timeout = 5

    # --------------------------------------------------
    # Public Methods
    # --------------------------------------------------
    def search_google(self, query: str) -> Dict[str, object]:
        """
        Search on Google.
        """
        query = query.strip()

        if not query:
            return self._response(
                False,
                "Search query is empty."
            )

        url = self.google_base + urllib.parse.quote_plus(query)
        return self.open_url(url, "Google search opened.")

    def search_youtube(self, query: str) -> Dict[str, object]:
        """
        Search on YouTube.
        """
        query = query.strip()

        if not query:
            return self._response(
                False,
                "Search query is empty."
            )

        url = self.youtube_base + urllib.parse.quote_plus(query)
        return self.open_url(url, "YouTube search opened.")

    def open_website(self, domain: str) -> Dict[str, object]:
        """
        Open website from domain name.
        Example:
        github.com
        openai.com
        """
        domain = domain.strip().lower()

        if not domain:
            return self._response(
                False,
                "Domain is empty."
            )

        if not domain.startswith("http://") and not domain.startswith("https://"):
            url = f"https://{domain}"
        else:
            url = domain

        return self.open_url(url, "Website opened.")

    def open_url(
        self,
        url: str,
        success_message: str = "URL opened."
    ) -> Dict[str, object]:
        """
        Open any valid URL.
        """
        try:
            webbrowser.open(url)

            return self._response(
                True,
                success_message,
                url=url
            )

        except Exception as exc:
            return self._response(
                False,
                str(exc)
            )

    def check_connection(self) -> Dict[str, object]:
        """
        Check internet connectivity.
        """
        try:
            requests.get(
                "https://www.google.com",
                timeout=self.default_timeout
            )

            return self._response(
                True,
                "Internet connection available."
            )

        except Exception:
            return self._response(
                False,
                "No internet connection."
            )

    def open_common_site(self, name: str) -> Dict[str, object]:
        """
        Open common platforms quickly.
        """
        sites = {
            "youtube": "https://youtube.com",
            "facebook": "https://facebook.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "chatgpt": "https://chat.openai.com",
            "linkedin": "https://linkedin.com",
            "twitter": "https://x.com",
            "instagram": "https://instagram.com"
        }

        key = name.strip().lower()

        if key not in sites:
            return self._response(
                False,
                "Unknown website."
            )

        return self.open_url(
            sites[key],
            f"{name.title()} opened."
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def _response(
        self,
        success: bool,
        message: str,
        url: Optional[str] = ""
    ) -> Dict[str, object]:
        return {
            "success": success,
            "message": message,
            "url": url
        }


# --------------------------------------------------
# Local Test
# --------------------------------------------------
if __name__ == "__main__":
    browser = BrowserService()

    print(browser.check_connection())
    print(browser.search_google("Python FastAPI tutorial"))