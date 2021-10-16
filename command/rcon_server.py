from mcrcon import MCRcon

from const import RCON_HOST, RCON_PASSWORD, RCON_PORT, RCON_TIMEOUT


class RconServer:

    def __init__(self):
        self.__session = MCRcon(host=RCON_HOST, password=RCON_PASSWORD, port=RCON_PORT, timeout=RCON_TIMEOUT)

    def connect(self):
        self.__session.connect()

    def reconnect(self, session):
        self.__session = session

    def exec(self, cmd):
        print(self.__session)
        self.__session.command(cmd)

    def disconnect(self):
        self.__session.disconnect()

    @property  # @propertyとすると、ageプロパティのgetterとして定義できる
    def session(self):
        return self.__session

    @session.setter  # nameプロパティのsetterとして定義する
    def session(self, value):
        print("setterを呼び出しました")
        self.__session = value  # privateの変数、__nameを設定する


rcon = RconServer()
