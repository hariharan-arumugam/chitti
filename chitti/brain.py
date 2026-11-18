"""Chitti's brain: an LLM that remembers the conversation.

Lesson 3: a chat with an LLM is a list of messages. Every turn we send the
whole list again, which is how the model "remembers". The system prompt is
where the product's personality and rules live.
"""
from pathlib import Path

import anthropic

MODEL = "claude-haiku-5-5"  # fast and cheap; good for a voice loop

# The persona lives in its own file so you can edit it without touching code.
SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.txt").read_text(encoding="utf-8")


class Brain:
    def __init__(self) -> None:
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
        self.history: list[dict] = []

    def reply(self, user_text: str) -> str:
        self.history.append({"role": "user", "content": user_text})
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=self.history,
        )
        answer = response.content[0].text
        self.history.append({"role": "assistant", "content": answer})
        return answer
