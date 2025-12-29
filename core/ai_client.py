"""Unified AI client for Claude and Gemini with PDF/image support"""
from typing import Literal
import anthropic
from google import genai
from google.genai import types


class AIClient:
    """Wrapper for Claude and Gemini APIs with multimodal support"""

    def __init__(self, claude_key: str = None, gemini_key: str = None):
        self.claude_key = claude_key
        self.gemini_key = gemini_key
        self._claude_client = None
        self._gemini_client = None

    @property
    def claude(self):
        if not self._claude_client and self.claude_key:
            self._claude_client = anthropic.Anthropic(api_key=self.claude_key)
        return self._claude_client

    @property
    def gemini(self):
        if not self._gemini_client and self.gemini_key:
            self._gemini_client = genai.Client(api_key=self.gemini_key)
        return self._gemini_client

    def chat(
        self,
        prompt: str,
        model_provider: Literal["claude", "gemini"] = "gemini",
        system_prompt: str = None
    ) -> str:
        """Send chat request to selected AI model.

        Args:
            prompt: User prompt
            model_provider: "claude" or "gemini"
            system_prompt: Optional system instructions

        Returns:
            AI response text
        """
        if model_provider == "claude":
            return self._chat_claude(prompt, system_prompt)
        else:
            return self._chat_gemini(prompt, system_prompt)

    def chat_with_pdf(
        self,
        prompt: str,
        pdf_bytes: bytes,
        model_provider: Literal["claude", "gemini"] = "gemini"
    ) -> str:
        """Send chat request with PDF file to AI model.

        Args:
            prompt: User prompt
            pdf_bytes: PDF file content as bytes
            model_provider: "claude" or "gemini"

        Returns:
            AI response text
        """
        if model_provider == "claude":
            return self._chat_claude_with_pdf(prompt, pdf_bytes)
        else:
            return self._chat_gemini_with_pdf(prompt, pdf_bytes)

    def chat_with_images(
        self,
        prompt: str,
        images_b64: list[str],
        model_provider: Literal["claude", "gemini"] = "gemini"
    ) -> str:
        """Send chat request with images to AI model.

        Args:
            prompt: User prompt
            images_b64: List of base64 encoded PNG images
            model_provider: "claude" or "gemini"

        Returns:
            AI response text
        """
        if model_provider == "claude":
            return self._chat_claude_with_images(prompt, images_b64)
        else:
            return self._chat_gemini_with_images(prompt, images_b64)

    def _chat_claude(self, prompt: str, system_prompt: str = None) -> str:
        """Chat with Claude API"""
        if not self.claude:
            raise ValueError("Claude API key not configured")

        messages = [{"role": "user", "content": prompt}]

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            system=system_prompt or "You are a helpful assistant.",
            messages=messages
        )

        return response.content[0].text

    def _chat_claude_with_pdf(self, prompt: str, pdf_bytes: bytes) -> str:
        """Chat with Claude API using PDF (via base64)"""
        if not self.claude:
            raise ValueError("Claude API key not configured")

        import base64
        pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_b64
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }]

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            messages=messages
        )

        return response.content[0].text

    def _chat_claude_with_images(self, prompt: str, images_b64: list[str]) -> str:
        """Chat with Claude API using images"""
        if not self.claude:
            raise ValueError("Claude API key not configured")

        content = []
        for img_b64 in images_b64:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": img_b64
                }
            })
        content.append({"type": "text", "text": prompt})

        messages = [{"role": "user", "content": content}]

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            messages=messages
        )

        return response.content[0].text

    def _chat_gemini(self, prompt: str, system_prompt: str = None) -> str:
        """Chat with Gemini API"""
        if not self.gemini:
            raise ValueError("Gemini API key not configured")

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self.gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        return response.text

    def _chat_gemini_with_pdf(self, prompt: str, pdf_bytes: bytes) -> str:
        """Chat with Gemini API using PDF directly"""
        if not self.gemini:
            raise ValueError("Gemini API key not configured")

        # Gemini supports PDF natively via inline_data
        contents = [
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            prompt
        ]

        response = self.gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        return response.text

    def _chat_gemini_with_images(self, prompt: str, images_b64: list[str]) -> str:
        """Chat with Gemini API using images"""
        if not self.gemini:
            raise ValueError("Gemini API key not configured")

        import base64
        contents = []

        for img_b64 in images_b64:
            img_bytes = base64.b64decode(img_b64)
            contents.append(
                types.Part.from_bytes(data=img_bytes, mime_type="image/png")
            )

        contents.append(prompt)

        response = self.gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        return response.text
