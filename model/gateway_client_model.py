class GatewayClientModel:

    def __init__(self, con):
        self.__con = con

    def send_view_chat_command(self, chat):
        con = self.__con
        data = chat.json()
