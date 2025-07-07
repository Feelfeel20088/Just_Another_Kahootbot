# Just Another Kahoot Bot

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Feelfeel20088/Just_Another_Kahootbot)


Just_Another_Kahoot_Bot is a completely scalable, single-threaded Kahoot bot designed for deployment on Kubernetes. It uses raw WebSockets, which improve reliability and performance. 

## Features
- **Scalable**: The bot is designed to handle multiple Kahoot sessions simultaneously, meaning a single instance can manage multiple client requests and flood several Kahoot games at once. Pair it with an ingress controller and replicas, and you've got a fully scalable Kahoot bot.
- **Single-Threaded**: The bot operates efficiently in a single thread, ensuring optimal performance without any loss of speed or reliability.
- **WebSocket-Based**: Unlike Selenium-based bots, which rely on web scraping, this bot uses raw WebSockets for faster, more reliable communication with Kahoot servers.
- **Reliability**: Selenium-based bots often rely on scraping dynamic elements (like buttons or input boxes), which can break whenever Kahoot updates their frontend. WebSockets provide a much more stable and dependable way of interacting with the platform, avoiding this pitfall.
- **Kubernetes-Ready**: Easily deployable on Kubernetes clusters, Docker compose or any other containtaer runtime that uses docker.
- **Docker Support**: A pre-configured Docker image is provided, simplifying deployment and making it easier to get started quickly.
- **Web Interface**: Coming soon – stay tuned for a simple, intuitive web interface for controlling the bot. If you're planning to build a web interface, check out the [Contributing.md](CONTRIBUTING.md).
- **API Access**: Full API documentation is available for programmatically interacting with the bot. 


## Kahoot-Related Features

- **Flood Games**: The bot can flood games by adding multiple bots to a single game, overwhelming the session and increasing the chaos.
- **God Mode**: In this mode, the bot answers all questions correctly, achieving a perfect 1000 score every time. Note that this mode is resource-intensive, so if you plan to allow users to spawn multiple of these bots, make sure to set limits to prevent overload.
- **Stealth Mode**: The bot still answers all questions correctly but with a slight delay, resulting in a score between 750 and 1000 points per round. This mode allows you to remain more under the radar while still outscoring most players.
- **Crasher Mode**: This exploits a bug in Kahoot that has yet to be patched despite @Feelfeel20088 making a bug report. Please use this feature responsibly and avoid being too disruptive.





## API Documentation

The API documentation is available at: [API Docs](https://felixhub.dev/Just_Another_Kahootbot:documentation)


## Installation Instructions

You have three main options for installing and running the bot:

### Option 1: Deploy using the Helm chart  
If you're running a Kubernetes cluster, this is probably the best option for you.

### Option 2: Pull or build the Docker container and deploy to any sort of container runtime  
If you're not running a cluster, this is likely the better option.

### Option 3: Deploy locally on any computer by just calling the init script  
Not really recommended for production use, but it could work for testing or development.

---

### Step 1 (for all options): Clone the Repository
```bash
git clone https://github.com/Feelfeel20088/Just_Another_Kahootbot.git --branch main
cd Just_Another_Kahootbot
```

### Option 1 Steps:

#### Step 1: Modify values.yaml to your liking. 
```bash
cd deployments
your_text_editor values.yaml
```

#### Step 2: Deploy the helm chart. 
```bash
helm upgrade --install kahootbot ./ -f values.yaml
```

#### Step 3: Check if it deployed correctly.
```bash 
kubectl get pods
```

### Option 2 Steps: 

#### Step 1: Pull or build the image.
You can pull the image like this:
```yaml
image:
  repository: Feelfeel200088/just_another_kahootbot
  tag: latest
```
Or to build the Docker container, run the following command in the project's root directory:
```bash
docker build -t <Your User/Gamertag>/just_another_kahootbot .
```

Once built, push the container to a registry like Docker Hub or Harbor if you have it on your cluster.
```bash
docker push <Your User/Gamertag>/just_another_kahootbot
```

#### Step 2: Deploy.
You can deploy however you want if u want to create a deployment.yaml, run it on compose, or just run it on a docker cluster thats up to u. if you need insterpation check out the helms chat templetes


### Option 3 Steps: 

#### step 1: Run the program. 
Go to the parent dir of the bot and run the program like this: 
```bash
cd ../
python -m Just_Another_Kahoot_Bot # or what ever you cloned the bot as
```



