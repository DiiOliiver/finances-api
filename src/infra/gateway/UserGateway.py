from email.message import EmailMessage

from aiosmtplib import send
from redis.asyncio import Redis

from application.gateway import (
    IUserGateway,
)
from infra.config.settings import Settings

settings = Settings()

redis = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)


class UserGateway(IUserGateway):
    def __init__(self):
        self.enabled = settings.EMAIL_ENABLED
        self.sender = settings.EMAIL_SENDER
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USERNAME
        self.smtp_pass = settings.SMTP_PASSWORD
        self.max_emails_per_hour = settings.EMAIL_LIMIT_PER_HOUR

    async def _can_send_email(self, email: str) -> bool:
        key = f'email_limit:{email}'
        count = await redis.get(key)

        if count is None:
            # Cria contador com TTL de 1 hora
            await redis.set(key, 1, ex=3600)
            return True

        if int(count) < self.max_emails_per_hour:
            await redis.incr(key)
            return True

        return False

    async def send_welcome_email(self, recipient: str, name: str):
        if not self.enabled:
            print('[Gateway] Envio de e-mail desabilitado.')
            return

        if not await self._can_send_email(recipient):
            print(f'[Gateway] Limite de e-mails excedido para: {recipient}')
            return

        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = recipient
        message['Subject'] = 'Bem-vindo ao sistema!'
        content = f'Olá {name},\n\nSeja bem-vindo! Obrigado por se cadastrar.'
        message.set_content(content)

        try:
            await send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_pass,
                start_tls=True,
            )
            print(f'[Gateway] E-mail enviado com sucesso para {recipient}.')
        except Exception as e:
            print(f'[Gateway] Erro ao enviar e-mail: {e}')
