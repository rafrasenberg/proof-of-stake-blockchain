from blockchain.node import Node

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run blockchain node.")
    parser.add_argument(
        "--ip",
        required=True,
        type=str,
        help="The node IP address. Use 0.0.0.0 in Docker, and localhost for native.",
    )
    parser.add_argument(
        "--node_port",
        required=True,
        type=int,
        help="The port used for P2P communication between nodes.",
    )
    parser.add_argument(
        "--api_port",
        required=True,
        type=int,
        help="Port on which the Node API runs.",
    )
    parser.add_argument(
        "--key_file",
        required=False,
        type=str,
        default=None,
        help="The path to the key file of the node (optional).",
    )
    args = parser.parse_args()

    node = Node(args.ip, args.node_port, args.key_file)

    node.start_p2p()
    node.start_node_api(args.api_port)
