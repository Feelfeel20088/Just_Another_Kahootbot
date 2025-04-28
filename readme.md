# Just Another Kahoot Bot

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Feelfeel20088/Just_Another_Kahootbot)


Just_Another_Kahoot_Bot is a completely scalable, single-threaded Kahoot bot designed for deployment on Kubernetes. And even better, it's not a shitty one that uses Selenium – it uses raw WebSockets, which improve reliability and performance. It can be easily connected to a web interface for control.

## Keywords
- Python
- Kahoot Bot
- Kahoot
- Kahoot Hack
- K3s
- Kubernetes
- Docker


## Features
- **Scalable**: The bot is designed to handle multiple Kahoot sessions simultaneously, meaning a single pod can manage multiple client requests and flood several Kahoot games at once. Pair it with an ingress controller and replicas, and you've got a fully scalable Kahoot bot.
- **Single-Threaded**: The bot operates efficiently in a single thread, ensuring optimal performance without any loss of speed or reliability.
- **WebSocket-Based**: Unlike Selenium-based bots, which rely on web scraping, this bot uses raw WebSockets for faster, more reliable communication with Kahoot servers.
- **Reliability**: Selenium-based bots often rely on scraping dynamic elements (like buttons or input boxes), which can break whenever Kahoot updates their frontend. WebSockets provide a much more stable and dependable way of interacting with the platform, avoiding this common pitfall.
- **Kubernetes-Ready**: Easily deployable on Kubernetes clusters, enabling seamless scaling and management of multiple instances of the bot.
- **Docker Support**: A pre-configured Docker image is provided, simplifying deployment and making it easier to get started quickly.
- **Web Interface**: Coming soon – stay tuned for a simple, intuitive web interface for controlling the bot. If you're planning to build a web interface, check out the [Contributing.md](CONTRIBUTING.md).
- **API Access**: Full API documentation is available for programmatically interacting with the bot. 
- **K3s Compatibility**: This bot is fully compatible with lightweight Kubernetes clusters like K3s, making it an excellent choice for small-scale deployments.

## Kahoot-Related Features

- **Flood Games**: The bot can flood games by adding multiple bots to a single game, overwhelming the session and increasing the chaos.
- **God Mode**: In this mode, the bot answers all questions correctly, achieving a perfect 1000 score every time. Note that this mode is resource-intensive, so if you plan to allow users to spawn multiple of these bots, make sure to set limits to prevent overload.
- **Stealth Mode**: The bot still answers all questions correctly but with a slight delay, resulting in a score between 750 and 1000 points per round. This mode allows you to remain more under the radar while still outscoring most players.
- **Crasher Mode**: This exploits a bug in Kahoot that has yet to be patched despite @Feelfeel20088 making a bug report. Please use this feature responsibly and avoid being too disruptive.





## API Documentation

The API documentation is available at: [API Docs](https://distinct-cicada-mildly.ngrok-free.app/Just_Another_Kahootbot:documentation)


## Installation Instructions

### Option 1: Deploy Using `deployment.yaml`
If you prefer to deploy directly using the provided `deployment.yaml`, download it to your machine and skip to the **Deployment** section below.

### Option 2: Clone the Repository
To manually set up the bot, start by cloning the repository:
```bash
git clone https://github.com/Feelfeel20088/Just_Another_Kahootbot.git --branch main
cd Just_Another_Kahootbot
```

## Building the Docker Container

To build the Docker container, run the following command in the project's root directory:
```bash
docker build -t <Your User/Gamertag>/just_another_kahootbot .
```

Once built, push the container to a registry like Docker Hub or Harbor if you have it on your cluster.
```bash
docker push <Your User/Gamertag>/just_another_kahootbot
```

Then change the repository location in the values.yaml file:
```yaml
image:
  repository: <Your User/Gamertag>/just_another_kahootbot
  tag: <YourTag>
```

## Deployment

In the root Deploy the application using:
```bash
helm upgrade --install deployments -f deployments/values.yaml
```

### Verifying Deployment
To check if the pod is running in a specific namespace, use:
```bash
kubectl get pods -n <namespace>
```

Once deployed, the bot should be up and running. If you encounter any issues, verify that the pod is running properly and check the logs using:
```bash
kubectl get pods -f <namespace>
kubectl logs -f <pod-name>
```

Happy botting! 🎉

