from .chat import ChatManager
from .api import API


class HyperChat:

    def __init__(self, token):
        self.host = "86.127.254.51:8519"
        self.ssl = False
        self.token = token
        self.rutas = {}
        self.api = API(self.host, self.token, ssl_active=self.ssl)
        self.chat_manager = None

    def run(self, app_functions):
        self.rutas = app_functions
        self.chat_manager = ChatManager(self, self.host, self.token, self.api.lista_canales(), ssl_active=self.ssl)

    def send(self, request, mensaje):
        token = request.get("channel")
        chat = self.chat_manager.chat(token)
        chat.enviar(mensaje)
