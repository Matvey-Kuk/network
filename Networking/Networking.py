from threading import Timer

from Networking.Peer import *
from Networking.ServerThread import *


class Networking(object):
    """ Этот класс обеспечивает все сетевое взаимодействие."""

    def __init__(self, host, port):
        self.peers = []
        self.server_thread = ServerThread(host, port, self.peers)
        self.server_thread.start()
        self.network_using_objects = []

        self.t = Timer(1, self.print_peers)
        self.t.start()

    @staticmethod
    def data_received_from_peer(peer, self):
        print("data received from peer")

    def send_data_to_peer(self, peer, data):
        pass

    @staticmethod
    def connection_closed(peer):
        print("connection closed")

    def send_data(self, peer, module_name):
        pass

    def get_data(self, module_name):
        return {
            "peer": Peer,
            "data": "some data"
        }

    def get_self_connection_data(self):
        return {
            "ip": "some ip",
            "port": "some port",
            "alive": True
        }

    def register_network_user(self, obj):
        """Здесь нужно решистрировать все объекты, использующие соединение"""
        pass

    def unregister_network_user(self, obj):
        """Здесь нужно разрегистрировать все объекты, которые больше не будут использовать соединение"""
        pass

    def collect_needed_peers(self):
        """Собирает всех пиров, с которыми нужно поддерживать соединение"""
        pass

    def inspect_connections(self):
        """Инспектирует все соединения- доотправляет данные и закрывает ненужные"""
        pass

    def provoke_connection(self, ip, port):
        """
        Провоцирует соединение
        @return: Peer object
        """
        return Peer

    def print_peers(self):
        print(self.peers)
        self.t = Timer(1, self.print_peers)
        self.t.start()
        pass