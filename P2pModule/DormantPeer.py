from time import time

from NetworkingModule.Peer import *


class DormantPeer():
    """
    Пир, о котором знает P2p модуль
    Хранит информацию о том, какой пир о нем сообщил и когда последний раз о нем сообщили
    """

    def __init__(self, reported_by_peer, ip, server_port):
        self.detection_time = 0
        self.reported_by_peers = []
        self.ip = ip
        self.server_port = server_port
        self.detected(reported_by_peer)

    def detected(self, peer):
        if not peer in self.reported_by_peers:
            self.reported_by_peers.append(peer)
        self.detection_time = time()

    def get_peers_reported(self):
        return self.reported_by_peers