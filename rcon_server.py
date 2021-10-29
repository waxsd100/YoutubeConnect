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
        self.__session.command(cmd)

    def disconnect(self):
        self.__session.disconnect()

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session):
        self.__session = session
