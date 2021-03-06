import argparse
import signal

from NetworkingModule.Networking import *
from P2pModule.P2p import *
from RequestsModule.RequestsProcessor import *
from ConnectionCircleDetectionModule.ConnectionCircleDetector import *
from Interface.Interface import *
from UsersDatabaseModule.UsersDatabase import *
from Interface.AllowingProcessing import *
from SelfIpDetectingModule.SelfIpDetector import *
from FunctionalTestInteractionModule.FunctionalTestInteraction import *


class Main(object):
    """Это основной класс, через который запускается приложение."""

    def __init__(self):
        AllowingProcessing().allow_processing = True

        self.command_line_arguments = self.parse_arguments()
        self.networking = self.start_networking()
        self.requests_processor = RequestsProcessor(self.networking)

        if self.command_line_arguments.UsersDatabaseModule:  #Запуск базы данных, если задан параметр
            self.self_ip_detector = SelfIpDetector(self.networking, self.requests_processor)
            self.users_database = UsersDatabase(self.networking, self.requests_processor, self.self_ip_detector)

        if self.command_line_arguments.P2PModule:  #Запуск пир-к-пиру модлуля, если заданы параметры
            self.connection_circle_detector = ConnectionCircleDetector(self.networking, self.requests_processor)
            self.p2p = P2p(self.networking, self.requests_processor, self.connection_circle_detector)

        if self.command_line_arguments.Interface:  #Запуск интерфейса, если задан параметр
            self.interface = Interface()
            self.interface.roottk.mainloop()

        if not self.command_line_arguments.functional_test_interaction_port is None:
            self.functional_tests_interactor = FunctionalTestInteraction(
                self.command_line_arguments.functional_test_interaction_port
            )

    @staticmethod
    def parse_arguments():
        """
        Создание парсеров, тех самых заветных параметров, но с очень малоинформирующей справкой, да к тому же на буржуйском :)
        """
        parser = argparse.ArgumentParser(description='Hello, p2p world.')
        parser.add_argument('-port', '-p', dest='port', help='Server port')
        parser.add_argument('-host', dest='bind_host', help='Host for server binding')
        parser.add_argument('-peer', dest='first_peer', help='ip:port of first peer needed for connection')
        parser.add_argument('-functionalTestInteractionPort', dest='functional_test_interaction_port', help='Enter port to set interaction with functional tests engine.')
        parser.add_argument(
            '-AuthDatabaseModule',
            dest='AuthDatabaseModule',
            action='store_true',
            help='Enables this module.'
        )
        parser.add_argument(
            '-UsersDatabaseModule',
            dest='UsersDatabaseModule',
            action='store_true',
            help='Enables this module.'
        )
        parser.add_argument(
            '-P2PModule',
            dest='P2PModule',
            action='store_true',
            help='Enables this module.'
        )

        parser.add_argument(
            '-Interface',
            dest='Interface',
            action='store_true',
            help='Enables interface module.'
        )
        command_line_args = parser.parse_args()
        return command_line_args

    def start_networking(self):
        """
        Задание параметров соединения по умолчанию, если они не указаны ( можно было сделать с помощью argparse)
        """
        port = 1234
        if not self.command_line_arguments.port is None:
            port = int(self.command_line_arguments.port)

        bind_host = "0.0.0.0"
        if not self.command_line_arguments.bind_host is None:
            bind_host = int(self.command_line_arguments.bind_host)

        print("Server started, connection point:\"" + bind_host + ":" + str(port) + "\"")

        networking = Networking(bind_host, port)

        if not self.command_line_arguments.first_peer is None:
            ip_port = self.command_line_arguments.first_peer.split(':')
            peer_ip = ip_port[0]
            peer_port = ip_port[1]
            networking.provoke_connection(peer_ip, int(peer_port))

        return networking

main = Main()


def signal_handler(signal, frame):
        print('Kill signal handled. Saving...')
        AllowingProcessing().allow_processing = False

signal.signal(signal.SIGINT, signal_handler)
