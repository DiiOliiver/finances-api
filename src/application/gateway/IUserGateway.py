from abc import ABC


class IUserGateway(ABC):
    async def _can_send_email(self, email: str) -> bool:
        pass

    async def send_welcome_email(self, recipient: str, name: str):
        pass
