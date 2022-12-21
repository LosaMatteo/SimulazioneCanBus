from typing import Optional


class Message(object):

    def __init__(
            self,
            id: int = 0,
            rtr: bool = False,
            ide: bool = False,
            r0: bool = False,
            dlc: Optional[int] = None,
            data: list = None,
            crc: int = 0,
            ack: int = 0
    ):
        self.ack = ack
        self.crc = crc
        self.data = data
        self.dlc = dlc
        self.r0 = r0
        self.ide = ide
        self.rtr = rtr
        self.id = id
