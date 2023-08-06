from .chat import ChatManager
from .api import API
from functools import wraps
import asyncio


class HyperChat:

    def __init__(self, token):
        self.host = "86.127.254.51:8519"
        self.ssl = False
        self.token = token
        self.rutas = {}
        self.api = API(self.host, self.token, ssl_active=self.ssl)
        self.chat_manager = None

    def run(self):
        self.chat_manager = ChatManager(self, self.host, self.token, self.api.lista_canales(), ssl_active=self.ssl)
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        finally:
            loop.close()

    def handler(self, commands: list):
        def decorator(f):
            @wraps(f)
            def wrapper(*args):
                f(*args)
            for comm in commands:
                self.rutas[comm] = wrapper
            return wrapper
        return decorator

    def send(self, request, mensaje):
        token = request.get("channel")
        chat = self.chat_manager.chat(token)
        chat.enviar(mensaje)
