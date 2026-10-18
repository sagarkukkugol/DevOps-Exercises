# Exercise 3: Scaling Flask App on a Single Node Using ReplicaSets

## Real-Life Tech Use Case: E-commerce Flash Sale

During a flash sale on an e-commerce website, such as Flipkart's Big Billion Days or Amazon Prime Day, the number of users accessing the application can increase rapidly.

For example, a Flask application might normally handle 100 requests per minute, but during a sale, traffic could increase to 10,000 requests per minute.

If the application runs inside a single Pod, that Pod may become overloaded and stop responding.

Kubernetes ReplicaSets help maintain multiple identical copies of the application. By increasing the number of replicas, Kubernetes can run more application Pods to handle incoming traffic.

For this exercise, a Flask application is deployed on a single-node Minikube cluster. The application is initially deployed with 3 replicas and then scaled to 5 replicas. The Kubernetes Service provides access to the application, and the ReplicaSet automatically replaces deleted Pods.

**Note:** A ReplicaSet maintains the desired number of Pods, but it does not automatically increase or decrease replicas based on traffic. Scaling is performed manually in this exercise. Automatic scaling based on resource usage requires a Horizontal Pod Autoscaler or another autoscaling mechanism.

---

## 1. Objectives

- Understand Kubernetes Pods and ReplicaSets.
- Develop a Flask application that simulates flash sale purchases.
- Build a Docker image for the Flask application.
- Deploy the application on a single-node Minikube cluster.
- Create a ReplicaSet to manage application Pods.
- Scale the application from 3 replicas to 5 replicas.
- Observe Pod creation and distribution across a node.
- Demonstrate self-healing by deleting a Pod.
- Expose the application using a Kubernetes Service.
- Test the application using port forwarding.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web framework |
| Docker | Containerization |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| kubectl | Kubernetes command-line tool |
| YAML | Kubernetes resource configuration |
| Gunicorn | Python application server |
| VS Code | Development environment |

---

## 3. Understanding Pods and ReplicaSets

### What is a Pod?

A Pod is the smallest deployable unit in Kubernetes. It contains one or more containers that run an application.

In this exercise, each Pod runs one container containing the Flask Flash Sale application.

### What is a ReplicaSet?

A ReplicaSet is a Kubernetes resource that maintains a specified number of identical application Pods.

For example:

```yaml
spec:
  replicas: 3
```

This instructs Kubernetes to maintain 3 application Pods.

If one Pod is deleted, the ReplicaSet detects that only 2 Pods remain and creates a replacement.

### What is a Kubernetes Service?

A Service provides a stable network endpoint for accessing application Pods.

The `flashsale-svc` Service selects Pods with the label `app: flashsale` and forwards requests to their application containers on port 5000.

---

## 4. Project Structure

```text
Exercise-3/
│
├── app.py
├── Dockerfile
├── flashsale-replicaset.yaml
└── README.md
```

| File | Description |
|---|---|
| `app.py` | Flask application containing homepage, purchase, and health endpoints |
| `Dockerfile` | Instructions for building the application image |
| `flashsale-replicaset.yaml` | Kubernetes ReplicaSet and Service configuration |
| `README.md` | Project documentation and execution steps |

---

## 5. Create the Flask Application

Create a file named `app.py`.

```python
from flask import Flask, request
import socket
import time
import random

app = Flask(__name__)


@app.get("/")
def homepage():
    return {
        "message": "Welcome to Big Sale!",
        "pod": socket.gethostname(),
        "ts": time.time()
    }


@app.get("/buy")
def buy():
    item = random.choice([
        "Smartphone",
        "Shoes",
        "Headphones",
        "Laptop"
    ])

    user = request.args.get(
        "user",
        f"user{random.randint(1, 1000)}"
    )

    return {
        "status": "success",
        "item": item,
        "user": user,
        "served_by_pod": socket.gethostname(),
        "time": time.strftime("%H:%M:%S")
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "pod": socket.gethostname()
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### Application Details

| Endpoint | Description |
|---|---|
| `/` | Displays a welcome message and the Pod hostname |
| `/buy` | Simulates a flash sale purchase |
| `/health` | Returns the health status of the application |

The `/buy` endpoint selects a random product and accepts a user ID through a query parameter.

Example:

```text
/buy?user=123
```

The response includes the product name, user ID, purchase status, time, and the Pod that handled the request.

The Pod hostname helps observe which application replica responds to requests.

---

## 6. Create the Dockerfile

Create a file named `Dockerfile`.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask gunicorn

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "1", "--threads", "2"]
```

### Dockerfile Explanation

- `FROM python:3.11-slim` uses a lightweight Python base image.
- `WORKDIR /app` sets the working directory inside the container.
- `COPY app.py .` copies the Flask application into the image.
- `RUN pip install` installs Flask and Gunicorn.
- `EXPOSE 5000` documents the application's listening port.
- `CMD` starts the application using Gunicorn.

Gunicorn is used inside the Linux container to serve the Flask application.

---

## 7. Build the Docker Image

Open the terminal in the `Exercise-3` directory.

Build the Docker image:

```cmd
docker build -t flashsale:1.0 .
```

The image name is:

```text
flashsale:1.0
```

### Load the image into Minikube

Because this exercise uses a local Docker image, load it into Minikube:

```cmd
minikube image load flashsale:1.0
```

The Kubernetes Pods will use this image to run the application.

The image is loaded locally into Minikube; pushing it to Docker Hub is not required for this local exercise.

---

## 8. Start and Verify Minikube

If Minikube is already running and the node is Ready, you can skip the startup command.

Start Minikube if required:

```cmd
minikube start --nodes=1
```

Verify the Kubernetes node:

```cmd
kubectl get nodes
```

Expected result:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...   ...
```

The cluster should contain one Ready node.

**Important:** Do not run `minikube delete` unless you intentionally want to remove your existing cluster and its resources. The existing Minikube cluster can be reused for this exercise.

---

## 9. Create the Kubernetes ReplicaSet

Create a file named `flashsale-replicaset.yaml`.

The configuration contains:

- A ReplicaSet named `flashsale-rs`
- Initially 3 application replicas
- Readiness and liveness probes
- CPU and memory resource requests and limits
- A Service named `flashsale-svc`

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: flashsale-rs
  labels:
    app: flashsale

spec:
  replicas: 3

  selector:
    matchLabels:
      app: flashsale

  template:
    metadata:
      labels:
        app: flashsale

    spec:
      containers:
        - name: flashsale-container
          image: flashsale:1.0
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 5000

          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 2
            periodSeconds: 5

          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 10

          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"

            limits:
              cpu: "500m"
              memory: "256Mi"

---
apiVersion: v1
kind: Service

metadata:
  name: flashsale-svc

spec:
  selector:
    app: flashsale

  ports:
    - name: http
      port: 80
      targetPort: 5000

  type: ClusterIP
```

### Configuration Explanation

| Configuration | Purpose |
|---|---|
| `replicas: 3` | Maintains 3 application Pods initially |
| `matchLabels` | Identifies the Pods managed by the ReplicaSet |
| `image: flashsale:1.0` | Specifies the Docker image |
| `containerPort: 5000` | Application container port |
| `readinessProbe` | Checks whether the application is ready to receive traffic |
| `livenessProbe` | Checks whether the application is healthy |
| `resources.requests` | Specifies the minimum requested CPU and memory |
| `resources.limits` | Sets the maximum CPU and memory allowed |
| `ClusterIP` | Exposes the Service inside the Kubernetes cluster |

---

## 10. Apply the ReplicaSet Configuration

Apply the Kubernetes configuration:

```cmd
kubectl apply -f flashsale-replicaset.yaml
```

Expected output:

```text
replicaset.apps/flashsale-rs created
service/flashsale-svc created
```

If the resources already exist, Kubernetes may report that they were configured or unchanged.

Verify the ReplicaSet:

```cmd
kubectl get rs flashsale-rs
```

Expected initial result:

```text
NAME           DESIRED   CURRENT   READY
flashsale-rs   3         3         3
```

Verify the Pods:

```cmd
kubectl get pods -l app=flashsale
```

The output should show 3 application Pods.

---

## 11. Scale the ReplicaSet to 5 Replicas

Initially, the ReplicaSet maintains 3 Pods.

To increase the replica count to 5, execute:

```cmd
kubectl scale rs flashsale-rs --replicas=5
```

Expected output:

```text
replicaset.apps/flashsale-rs scaled
```

Verify the updated ReplicaSet:

```cmd
kubectl get rs flashsale-rs
```

Expected result:

```text
NAME           DESIRED   CURRENT   READY
flashsale-rs   5         5         5
```

Kubernetes creates 2 additional Pods to reach the desired replica count.

---

## 12. Verify the Updated Pods

Execute:

```cmd
kubectl get pods -l app=flashsale
```

Expected result:

```text
NAME                 READY   STATUS
flashsale-rs-2q28v   1/1     Running
flashsale-rs-m8cn5   1/1     Running
flashsale-rs-ndm5t   1/1     Running
flashsale-rs-tvnjm   1/1     Running
flashsale-rs-v5h9r    1/1     Running
```

Pod names may differ in your environment.

All 5 Pods should reach `1/1 Running` status.

---

## 13. Delete a Pod to Test Self-Healing

To demonstrate the self-healing behavior of Kubernetes, delete one of the application Pods.

First, list the Pods:

```cmd
kubectl get pods -l app=flashsale
```

Delete one Pod using its actual name:

```cmd
kubectl delete pod flashsale-rs-v5h9r
```

Expected output:

```text
pod "flashsale-rs-v5h9r" deleted
```

The ReplicaSet detects that the number of Pods is below the desired count of 5 and creates a replacement Pod.

Verify the Pods again:

```cmd
kubectl get pods -l app=flashsale
```

The new Pod will have a different generated name.

The ReplicaSet should eventually return to:

```text
DESIRED: 5
CURRENT:  5
READY:    5
```

In this exercise, two Pods were manually deleted. Kubernetes created replacement Pods and maintained the desired replica count of 5.

---

## 14. Observe Pod Distribution Across Nodes

To view Pod IP addresses and node placement:

```cmd
kubectl get pods -l app=flashsale -o wide
```

Example output:

```text
NAME                 READY   STATUS    IP            NODE
flashsale-rs-2q28v   1/1     Running   10.244.0.8    minikube
flashsale-rs-m8cn5   1/1     Running   10.244.0.6    minikube
flashsale-rs-ndm5t   1/1     Running   10.244.0.11   minikube
flashsale-rs-tvnjm   1/1     Running   10.244.0.5    minikube
flashsale-rs-v5h9r    1/1     Running   10.244.0.10   minikube
```

The exact Pod names and IP addresses may change.

All 5 Pods run on the same Minikube node because the cluster has only one node.

This demonstrates that multiple Pods can run on a single Kubernetes node, provided sufficient resources are available.

---

## 15. Access the Application Using a Kubernetes Service

The application is exposed using the `flashsale-svc` Service.

Verify the Service:

```cmd
kubectl get svc flashsale-svc
```

Example output:

```text
NAME            TYPE        CLUSTER-IP      PORT(S)
flashsale-svc   ClusterIP  10.97.199.178   80/TCP
```

Start port forwarding:

```cmd
kubectl port-forward service/flashsale-svc 8080:80
```

Expected output:

```text
Forwarding from 127.0.0.1:8080 -> 5000
Forwarding from [::1]:8080 -> 5000
```

Keep this terminal open while testing the application.

### Test the Homepage

Open the following URL in your browser:

```text
http://localhost:8080/
```

Expected response:

```json
{
  "message": "Welcome to Big Sale!",
  "pod": "flashsale-rs-m8cn5",
  "ts": 1792300000
}
```

The Pod hostname and timestamp will vary.

### Test the Purchase Endpoint

Open:

```text
http://localhost:8080/buy?user=123
```

Example response:

```json
{
  "item": "Headphones",
  "served_by_pod": "flashsale-rs-m8cn5",
  "status": "success",
  "time": "06:22:51",
  "user": "123"
}
```

The actual product, time, and Pod hostname may differ.

The `served_by_pod` field identifies which Pod handled the request.

---

## 16. Key Observations and Learnings

### Pod Distribution

Each Pod is an identical worker running the same Flask application.

Scaling the ReplicaSet creates additional copies of the application. In this exercise, 5 Pods were maintained on a single node.

### Resiliency

When an application Pod is deleted, the ReplicaSet automatically creates a replacement.

This maintains the desired number of application replicas.

### Efficiency

Scaling allows applications to run more or fewer Pods according to workload requirements.

However, this exercise uses manual scaling. Kubernetes does not automatically change the replica count merely because traffic increases or decreases.

### Service-Based Access

The Kubernetes Service provides a stable endpoint for accessing the application.

Requests sent to the Service can be routed to eligible application Pods, rather than requiring the user to connect to a particular Pod.

### Real-World Scalability

ReplicaSets are useful for maintaining application availability and replica counts.

For production applications, additional components such as Deployments, Horizontal Pod Autoscalers, resource monitoring, ingress controllers, and multi-node clusters may be required for more advanced scaling and availability.

---

## 17. Questions and Answers Based on the Exercise

### Q1. What is the initial number of replicas in the ReplicaSet?

**Answer:** 3 replicas.

### Q2. How many Pods are running after applying the ReplicaSet configuration?

**Answer:** 3 Pods, assuming all Pods are successfully created and become Ready.

### Q3. What happens when the ReplicaSet is scaled to 5 replicas?

**Answer:** Kubernetes creates 2 additional Pods to reach the desired replica count of 5.

### Q4. What happens when one Pod is deleted?

**Answer:** The ReplicaSet detects that the actual number of Pods is below the desired count and creates a replacement Pod.

### Q5. How does Kubernetes maintain the desired number of replicas?

**Answer:** The ReplicaSet controller continuously compares the desired number of replicas with the actual number of matching Pods. It creates or removes Pods as necessary to maintain the desired state.

### Q6. How many nodes are running in this exercise?

**Answer:** 1 node.

### Q7. Where are the Pods running?

**Answer:** All 5 application Pods are running on the single Minikube node.

### Q8. What is the purpose of a Kubernetes Service?

**Answer:** A Service provides a stable network endpoint and forwards traffic to matching application Pods.

### Q9. What is the purpose of the readiness probe?

**Answer:** The readiness probe checks whether the application is ready to receive traffic. A Pod that is not Ready is excluded from normal Service traffic.

### Q10. What is the purpose of the liveness probe?

**Answer:** The liveness probe checks whether the application is healthy. If the probe repeatedly fails, Kubernetes can restart the affected container.

### Q11. Does a ReplicaSet automatically scale based on traffic?

**Answer:** No. A ReplicaSet maintains the configured replica count. Automatic scaling based on metrics requires an autoscaling mechanism such as the Horizontal Pod Autoscaler.

### Q12. What is the difference between a ReplicaSet and a Deployment?

**Answer:** A ReplicaSet maintains the desired number of Pods. A Deployment manages ReplicaSets and provides additional features such as rolling updates and revision history.

---

## 18. Additional Challenges

1. Change the Flask application image to a different version and deploy it.
2. Create a Kubernetes Deployment instead of a standalone ReplicaSet.
3. Use `kubectl describe rs flashsale-rs` to inspect ReplicaSet events.
4. Use `kubectl logs <pod-name>` to inspect application logs.
5. Use `kubectl exec -it <pod-name> -- /bin/sh` to access a running container.
6. Scale the ReplicaSet down to 2 replicas:

   ```cmd
   kubectl scale rs flashsale-rs --replicas=2
   ```

7. Explore a Horizontal Pod Autoscaler to scale the application using resource metrics.
8. Run a load test to generate requests and observe application behavior.

---

## 19. Conclusion

This exercise demonstrates the deployment and scaling of a Flask application using Docker, Kubernetes, and Minikube.

The application was initially deployed with 3 replicas and then scaled to 5 replicas. When Pods were manually deleted, the ReplicaSet created replacement Pods to maintain the desired count.

The Kubernetes Service provided a stable endpoint for accessing the application, while the Pod hostname helped identify which replica handled a request.

The exercise demonstrates the fundamental concepts of container orchestration, replica management, manual scaling, service access, and self-healing in Kubernetes.
