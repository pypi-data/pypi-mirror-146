# -*- coding: utf-8 -*-
from socketio import Server


class SioServer:
    def __init__(self):
        self.sio: Server = Server()
