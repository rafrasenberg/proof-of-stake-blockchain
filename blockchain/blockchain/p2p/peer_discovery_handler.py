import os
import threading
import time

from blockchain.p2p.message import Message
from blockchain.utils.helpers import BlockchainUtils
from blockchain.utils.logger import logger


class PeerDiscoveryHandler:
    def __init__(self, node):
        self.socket_communication = node
        self.use_docker = os.environ.get("USE_DOCKER", False)

    def start(self):
        status_thread = threading.Thread(target=self.status, args=())
        status_thread.start()
        discovery_thread = threading.Thread(target=self.discovery, args=())
        discovery_thread.start()

    def status(self):
        count = 1
        while True:
            current_connections = []
            for peer in self.socket_communication.peers:
                current_connections.append(f"{peer.ip}: {peer.port}")
            if not self.socket_communication.peers:
                logger.info({"message": "No nodes connected"})
            else:
                logger.info(
                    {
                        "message": "Node connection status",
                        "connections": f"Current connections: {current_connections}",
                        "whoami": self.socket_communication,
                    }
                )
            count += 1
            sleep_time = 15 if count < 10 else 600  # prevent excessive logging
            time.sleep(sleep_time)

    def discovery(self):
        while True:
            handshake_message = self.handshake_message()
            self.socket_communication.broadcast(handshake_message)
            time.sleep(10)

    def handshake(self, connected_node):
        handshake_message = self.handshake_message()
        self.socket_communication.send(connected_node, handshake_message)

    def handshake_message(self):
        connector_self = self.socket_communication.socket_connector
        peers_self = self.socket_communication.peers
        data = peers_self
        message_type = "DISCOVERY"
        message = Message(connector_self, message_type, data)
        encoded_message = BlockchainUtils.encode(message)
        return encoded_message

    def handle_message(self, message):
        peers_socket_connector = message.sender_connector
        peers_peer_list = message.data

        if not any(
            peer.equals(peers_socket_connector)
            for peer in self.socket_communication.peers
        ):
            self.socket_communication.peers.append(peers_socket_connector)

        for peers_peer in peers_peer_list:
            peer_known = False

            for peer in self.socket_communication.peers:
                if peer.equals(peers_peer):
                    peer_known = True

            if not peer_known and not peers_peer.equals(
                self.socket_communication.socket_connector
            ):
                ip = peers_peer.ip
                if self.use_docker:
                    ip = peers_peer.docker_ip
                self.socket_communication.connect_with_node(ip, peers_peer.port)
