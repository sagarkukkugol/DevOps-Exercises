# Exercise 4: Docker Networking with Multiple Containers

## Real-Life Tech Use Case: E-commerce Web Application

An e-commerce website consists of several services that work together to process customer requests.

For example, during an online shopping session:

- The Flask web server receives requests from users.
- The MySQL database stores application data.
- The Redis cache stores frequently accessed information for faster retrieval.

These services run in separate Docker containers. Docker networking allows the containers to communicate with each other while maintaining network isolation from other containers.

In this exercise, a Flask REST API, a MySQL database, and a Redis cache are connected through a custom Docker bridge network named `my-bridge-net`.

The Flask application is accessible from the host machine using port 5001.

---

## 1. Objectives

- Understand Docker networking concepts.
- Create a custom Docker bridge network.
- Inspect the Docker network configuration.
- Develop a Flask REST API.
- Build a Docker image for the Flask application.
- Launch Flask, MySQL, and Redis containers.
- Configure communication between containers using container names.
- Test container-to-container network connectivity.
- Expose the Flask application's port to the host machine.
- Understand the difference between bridge and host networking.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web framework for the REST API |
| Docker | Containerization |
| Docker Bridge Network | Communication between containers |
| MySQL | Relational database container |
| Redis | In-memory cache container |
| VS Code | Development environment |

---

## 3. Understanding Docker Networking

### What is Docker Networking?

Docker networking allows containers to communicate with other containers and external systems.

Containers can be connected to different network types depending on the application's requirements.

### What is a Bridge Network?

A bridge network connects containers running on the same Docker host.

In this exercise, a custom bridge network named `my-bridge-net` is created.

The Flask container can communicate with the MySQL and Redis containers using their container names.

For example:

```text
Flask Container
      |
      | Docker Bridge Network
      |
      +---------- MySQL Container
      |
      +---------- Redis Container
```

### What is Container Name Resolution?

Containers connected to a custom Docker bridge network can resolve each other by container name.

For example:

```text
mysql
redis
```

The Flask container can use these names instead of hardcoding container IP addresses.

---

## 4. Project Structure

```text
Exercise-4/
│
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

| File | Description |
|---|---|
| `app.py` | Flask REST API application |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Instructions for building the Flask Docker image |
| `README.md` | Project documentation and execution steps |

---

## 5. Create the Docker Bridge Network

Create a custom bridge network named `my-bridge-net`.

```cmd
docker network create --driver bridge my-bridge-net
```

Example output:

```text
87c23b491f5994c74e497f4f4f4f4f4f4f4f4
```

The network ID will be different in your environment.

### Verify the Network

```cmd
docker network ls
```

Example output:

```text
NETWORK ID     NAME            DRIVER    SCOPE
87c23b491f59   my-bridge-net   bridge    local
```

### Inspect the Network

```cmd
docker network inspect my-bridge-net
```

The command displays network details such as:

- Network name
- Network ID
- Bridge driver
- Subnet
- Gateway
- Connected containers

Initially, the `Containers` section should be empty because no containers have been connected yet.

---

## 6. Create the Flask Application

Create a file named `app.py`.

```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/about", methods=["GET"])
def about():
    return jsonify({
        "name": "Simple REST API",
        "version": "1.0",
        "description": "This is a simple REST API built with Flask."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
```

### Application Details

| Endpoint | Description |
|---|---|
| `/about` | Returns information about the REST API |

The Flask application returns its name, version, and description in JSON format.

The application listens on port 5001.

The `host="0.0.0.0"` setting allows the Flask server to receive requests from outside the container.

---

## 7. Create requirements.txt

Create a file named `requirements.txt`.

```text
Flask>=3.0,<4.0
```

This file contains the Python dependency required by the Flask application.

---

## 8. Create the Dockerfile

Create a file named `Dockerfile`.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "app.py"]
```

### Dockerfile Explanation

| Instruction | Purpose |
|---|---|
| `FROM` | Uses a Python base image |
| `WORKDIR` | Sets the working directory inside the container |
| `COPY` | Copies application files into the image |
| `RUN` | Installs Flask |
| `EXPOSE` | Documents the application port |
| `CMD` | Starts the Flask application |

---

## 9. Build the Flask Docker Image

Open the terminal inside the `Exercise-4` directory.

Build the image:

```cmd
docker build -t flask-api:1.0 .
```

Example output:

```text
[+] Building ...
[+] Building ... FINISHED
```

Verify the image:

```cmd
docker images
```

The output should contain an image named:

```text
flask-api
```

with tag:

```text
1.0
```

---

## 10. Launch the MySQL Container

Start the MySQL container and connect it to the custom bridge network.

```cmd
docker run -d --name mysql --network my-bridge-net -e MYSQL_ROOT_PASSWORD=LabRoot123! mysql:8.4
```

### Command Explanation

- `-d` runs the container in the background.
- `--name mysql` assigns the container name.
- `--network my-bridge-net` connects the container to the custom bridge network.
- `MYSQL_ROOT_PASSWORD` sets a local lab password for MySQL.

Verify the container:

```cmd
docker ps
```

Check MySQL logs:

```cmd
docker logs mysql
```

Wait until MySQL has completed initialization and is ready to accept connections.

---

## 11. Launch the Redis Container

Start Redis on the same network.

```cmd
docker run -d --name redis --network my-bridge-net redis:7
```

Verify the container:

```cmd
docker ps
```

Redis is now connected to `my-bridge-net`.

---

## 12. Launch the Flask Container

Start the Flask container:

```cmd
docker run -d --name flask --network my-bridge-net -p 5001:5001 flask-api:1.0
```

### Command Explanation

| Option | Purpose |
|---|---|
| `-d` | Runs the container in the background |
| `--name flask` | Assigns the container name |
| `--network my-bridge-net` | Connects Flask to the custom network |
| `-p 5001:5001` | Maps host port 5001 to container port 5001 |
| `flask-api:1.0` | Specifies the Flask application image |

Verify all containers:

```cmd
docker ps
```

The following three containers should be running:

```text
mysql
redis
flask
```

---

## 13. Test the Flask Application

Open a browser and visit:

```text
http://localhost:5001/about
```

Expected response:

```json
{
    "description": "This is a simple REST API built with Flask.",
    "name": "Simple REST API",
    "version": "1.0"
}
```

The response confirms that the Flask application is accessible through the published host port.

---

## 14. Test Connectivity Between Containers

Docker's custom bridge network provides DNS-based container name resolution.

The Flask container should be able to resolve the MySQL and Redis container names.

### Test MySQL Name Resolution

Execute:

```cmd
docker exec flask python -c "import socket; print(socket.gethostbyname('mysql'))"
```

Example output:

```text
172.18.0.2
```

### Test Redis Name Resolution

Execute:

```cmd
docker exec flask python -c "import socket; print(socket.gethostbyname('redis'))"
```

Example output:

```text
172.18.0.3
```

The IP addresses may differ in your environment.

These commands confirm that Docker can resolve the container names to their network IP addresses.

This is a name-resolution test. It does not prove that MySQL or Redis is accepting application connections.

### Inspect the Network Again

```cmd
docker network inspect my-bridge-net
```

The network's `Containers` section should now list the Flask, MySQL, and Redis containers.

---

## 15. Understanding Port Mapping

The Flask container listens on port 5001.

The Docker command:

```cmd
docker run -d --name flask --network my-bridge-net -p 5001:5001 flask-api:1.0
```

maps the host port to the container port.

```text
Host Machine
    |
    | localhost:5001
    |
Docker Container
    |
    | Flask Application:5001
```

The application can therefore be accessed from the host machine using:

```text
http://localhost:5001/about
```

The MySQL and Redis containers do not need published host ports for this networking exercise because they are accessed through the internal Docker bridge network.

---

## 16. Key Observations and Learnings

### Docker Network Isolation

A custom bridge network provides network isolation from containers that are not connected to it.

Only containers connected to the same network can use that network's internal DNS names and communicate through it, subject to the container applications and firewall rules.

### Container Name Resolution

The Flask container can resolve the names `mysql` and `redis` to their corresponding container IP addresses.

This makes communication easier because applications do not need hardcoded IP addresses.

### Container Communication

Containers on the same bridge network can communicate directly using their container names and the destination service's listening port.

For example, MySQL normally listens on port 3306, while Redis normally listens on port 6379.

### Port Mapping

Docker's `-p` option publishes a container port on the host machine.

In this exercise, Flask is exposed through port 5001.

### Multi-Container Architecture

The application is separated into three containers:

- Flask handles HTTP requests.
- MySQL provides relational database functionality.
- Redis provides in-memory cache functionality.

This separation makes it easier to manage and scale each component independently.

---

## 17. Questions and Answers

### Q1. What is the purpose of the `--network` flag in `docker run`?

**Answer:** It connects a container to a specified Docker network so that the container can communicate with other containers on that network.

### Q2. How do containers communicate with each other on the same custom bridge network?

**Answer:** Containers communicate using their container names or IP addresses and the port on which the destination application is listening.

### Q3. What is the difference between a bridge network and a host network?

**Answer:**

- A bridge network provides an isolated network for containers and allows communication through the Docker bridge.
- A host network shares the host's network stack, removing the normal separate container network namespace on supported platforms.

### Q4. How can you expose a container's port to the host machine?

**Answer:** Use the `-p` option.

Example:

```cmd
docker run -d -p 5001:5001 flask-api:1.0
```

### Q5. Why do we use a custom bridge network?

**Answer:** A custom bridge network provides container name resolution, communication between connected containers, and network isolation.

### Q6. Why do we use container names instead of IP addresses?

**Answer:** Container IP addresses can change when containers are recreated. Container names provide a more stable way for applications to locate services on the same custom bridge network.

### Q7. What is the purpose of the Flask container in this exercise?

**Answer:** The Flask container runs the REST API and provides the `/about` endpoint to return application information.

### Q8. Why are MySQL and Redis separate containers?

**Answer:** They are independent services with different responsibilities. MySQL stores relational data, while Redis is an in-memory data store commonly used for caching.

### Q9. What is the difference between `EXPOSE` and `-p`?

**Answer:** `EXPOSE` documents the port used by an application inside the image. The `-p` option publishes a port on the host machine and makes it accessible from outside the container.

### Q10. Does this Flask application actually store data in MySQL or Redis?

**Answer:** No. The current `/about` endpoint only returns static JSON information. The containers are connected through the Docker network, but the Flask application has not been programmed to perform database or cache operations.

---

## 18. Additional Challenges

1. Add a new Flask endpoint named `/health` that returns the application health status.
2. Connect the Flask application to MySQL using a Python MySQL client.
3. Store application information in MySQL and retrieve it through a Flask endpoint.
4. Connect Flask to Redis and store a temporary cache value.
5. Publish MySQL or Redis ports to the host for local testing, while keeping them unpublished in normal deployments.
6. Use `docker inspect flask` to examine the network configuration.
7. Use `docker logs flask` to view application logs.
8. Use Docker Compose to start all three containers from one configuration file.
9. Compare communication between containers on a custom bridge network and the default bridge network.

---

## 19. Conclusion

This exercise demonstrates how to create and configure Docker networking for a multi-container application.

A custom bridge network named `my-bridge-net` was created, and the Flask, MySQL, and Redis containers were connected to it.

The Flask application was exposed to the host machine through port 5001. Container name resolution was tested to verify that Flask could locate MySQL and Redis through the custom bridge network.

The exercise demonstrates fundamental concepts of Docker networking, container isolation, name resolution, and port publishing.
