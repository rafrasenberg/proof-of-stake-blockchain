import os


class SocketConnector:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.use_docker = os.environ.get("USE_DOCKER", False)
        if self.use_docker:
            self.docker_ip = self.docker_node_mapping()[self.port]

    def get_docker_node_ports(self):
        return [int(i) for i in os.environ.get("DOCKER_NODE_PORTS", "").split(",")]

    def get_docker_node_container_names(self):
        return os.environ.get("DOCKER_NODE_CONTAINER_NAMES", "").split(",")

    def first_node_config(self):
        if self.use_docker:
            return {
                "port": self.get_docker_node_ports()[0],
                "ip": self.get_docker_node_container_names()[0],
            }
        return {"port": os.environ.get("FIRST_NODE_PORT", 8010), "ip": "localhost"}

    def docker_node_mapping(self):
        docker_node_ports = self.get_docker_node_ports()
        docker_node_container_names = self.get_docker_node_container_names()
        return {
            int(port): name
            for port, name in zip(docker_node_ports, docker_node_container_names)
        }

    def equals(self, connector):
        if connector.ip == self.ip and connector.port == self.port:
            return True
        return False
