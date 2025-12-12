from __future__ import annotations

from abc import ABC, abstractmethod

from modules.real_estate.application.dto.chatbot_dto import (
    ChatbotSearchCommand,
    ChatbotSearchResult,
)


class ChatbotSearchPort(ABC):

    @abstractmethod
    async def execute(self, cmd: ChatbotSearchCommand) -> ChatbotSearchResult:
        raise NotImplementedError