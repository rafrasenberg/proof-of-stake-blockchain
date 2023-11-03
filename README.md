![main workflow](https://github.com/rafrasenberg/proof-of-stake-blockchain/actions/workflows/pipeline.main.yml/badge.svg)

# Proof of Stake Blockchain in Python - Full Example

Features:

- Python 3.11
- Proof of Stake, with consensus algorithm
- P2P communication
- Node API with FastAPI, with separation of concern
- Flexible: use docker or native
- Unit tests + CI/CD through Github Actions

This is just a simple test project. Don't use any of it in production. 😅


## Running the blockchain nodes
```sh
docker compose up --build
```

This command will start 3 nodes, running on ports 8010, 8011, and 8012. 

If you want to run the nodes on different ports, change the `DOCKER_NODE_PORTS` variable for each node container. Make sure the order of the ports is always the same between different containers, the socket connector logic assumes it is. 

### Native
If you don't want to use Docker, you can alternatively run the nodes straight from your terminal. First, create a virtual environment and install the dependencies:

```sh
pip install -r blockchain/requirements/dev.txt
```

Now open up three terminal tabs, and run the following:

```sh
# Terminal 1
python run_node.py --ip=localhost --node_port=8010 --api_port=8050 --key_file=./keys/genesis_private_key.pem

# Terminal 2
python run_node.py --ip=localhost --node_port=8011 --api_port=8051 --key_file=./keys/staker_private_key.pem

# Terminal 3
python run_node.py --ip=localhost --node_port=8012 --api_port=8052
```

If you want to use different ports, make sure you provide a value for this variable in your terminal: `FIRST_NODE_PORT`. It defaults to `8010`, so therefore you won't need to specify it if you follow the example above.

## Adding transactions

To actually see the blockchain in action, you need to add some transactions. 

Run the following command:

```sh
python sample_transactions.py
```

This will add 7 transactions, with the current transaction pool set to 2 transactions per block, it will thus create 3 blocks and leave 1 transaction in the transaction pool. Visit `http://localhost:8050/api/v1/blockchain/` to view the blockchain!

## Docs

Visit the auto generated docs at the APIs of each that you run. Example: `http://localhost:8050/api/v1/docs/`

## Consensus algorithm

The PoS implementation uses a very simple lottery-like mechanism to select a validator from a list of stakers to forge the next block. Validators' chances of being selected are proportional to their stakes, and the offset from a reference hash value is used to determine the winner. The validator with the closest offset is chosen as the forger. This method aims to achieve a form of randomization while still giving validators with larger stakes a higher probability of being selected. 

## Logging

Basic JSON logging has been implemented for the nodes, as well as the API. You'll see the output in the logs when you run docker compose up.

### Datadog integration

In production you'd ideally want something like datadog, to capture your logs. Since our log output is already in JSON format, datadog integration becomes easy. You can test out the log connection locally through docker compose, uncommenting lines 61-72. Then copy the `.env.example`:

```sh
cp .env.example .env
```

Now update the `DD_API_KEY` variable, with your API key. 

If you'd run this in production, e.g. AWS ECS, you would do something very similar. Just run the datadog agent as a sidecar and use the same variables as in the `.env.example`, but put them in the task definition. Since the nodes log to `stdout`, the agent will pick it up. Make sure you add the appropriate docker labels to your node container so it gets picked up (`DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL` is set to `False`),

## Extra

Make sure the containers are running. Running this against node_one will update all nodes since docker makes use of a volume for the project root. 

Tests:

```sh
docker compose exec node_one pytest .
```

Lint:

```sh
docker compose exec node_one flake8 .
docker compose exec node_one black .
docker compose exec node_one isort --skip=env .
docker compose exec node_one bandit --configfile .bandit -r -ll .
```

Alternatively, if you run this natively. Just remove the `docker compose exec node_one` part before every command, make sure you are in the `blockchain` dir, and you are good to go.