import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


class AIEngine:
    """
    Core language engine for LIAO Assistant.

    Responsibilities:
    - Initialize model connection
    - Apply assistant behavior rules
    - Generate natural responses
    - Return structured intent data when needed
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError("Missing GEMINI_API_KEY in environment settings.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash"
        )

        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """
        Assistant personality and response policy.
        """
        return """
তুমি নীলিমা, LIAO Assistant-এর ব্যক্তিত্বভিত্তিক সহকারী।

তোমার আচরণ:
- সবসময় স্বাভাবিক, সুন্দর ও পরিষ্কার বাংলায় কথা বলবে।
- ব্যবহারকারীর সাথে আন্তরিক ও বন্ধুসুলভ আচরণ করবে।
- অপ্রয়োজনীয় বড় উত্তর দেবে না।
- প্রযুক্তিগত বিষয়ে দক্ষভাবে সাহায্য করবে।
- প্রয়োজন হলে ধাপে ধাপে নির্দেশনা দেবে।
- কম্পিউটার সম্পর্কিত কাজ হলে আত্মবিশ্বাসীভাবে সহায়তা করবে।
- তুমি চ্যাটবট নও, তুমি একটি স্মার্ট ডেস্কটপ সহকারী।

যদি ব্যবহারকারী কোনো কাজ করতে বলে, আগে উদ্দেশ্য বুঝবে।
যদি উত্তর সাধারণ কথোপকথন হয়, স্বাভাবিকভাবে উত্তর দেবে।
"""

    def _build_prompt(self, user_input: str, context: str = "") -> str:
        """
        Compose final prompt.
        """
        return f"""
System Instructions:
{self.system_prompt}

Conversation Context:
{context}

User Message:
{user_input}

Assistant Response:
"""

    def generate_response(self, user_input: str, context: str = "") -> str:
        """
        Return natural language response.
        """
        try:
            prompt = self._build_prompt(user_input, context)
            response = self.model.generate_content(prompt)

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            return "দুঃখিত, এই মুহূর্তে উত্তর তৈরি করা যায়নি।"

        except Exception:
            return "দুঃখিত, এখন সংযোগ সমস্যার কারণে উত্তর দেওয়া যাচ্ছে না।"

    def detect_intent(self, user_input: str) -> dict:
        """
        Detect task intent from user request.

        Example return:
        {
            "intent": "open_app",
            "target": "vscode",
            "message": "VS Code খুলছি।"
        }
        """
        try:
            prompt = f"""
নিচের ব্যবহারকারীর অনুরোধ বিশ্লেষণ করো।

শুধু JSON ফরম্যাটে উত্তর দাও।

Supported intents:
- chat
- open_app
- search_web
- create_file
- system_action

User Request:
{user_input}
"""

            response = self.model.generate_content(prompt)

            if hasattr(response, "text") and response.text:
                return json.loads(response.text.strip())

            return {
                "intent": "chat",
                "target": "",
                "message": ""
            }

        except Exception:
            return {
                "intent": "chat",
                "target": "",
                "message": ""
            }