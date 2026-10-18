# Exercise 3: Flask Flash Sale Application – Kubernetes ReplicaSet

## 1. Introduction

This project demonstrates how to deploy and scale a Flask web application using Docker and Kubernetes. A Kubernetes ReplicaSet maintains the desired number of application Pods and automatically creates replacement Pods when existing Pods are deleted or fail.

The Flash Sale application provides endpoints to check application status and simulate a product purchase.

## 2. Objectives

- Build and containerize a Flask application using Docker.
- Deploy the application on a Kubernetes cluster using Minikube.
- Create a Kubernetes ReplicaSet to manage application Pods.
- Scale the application from 3 replicas to 5 replicas.
- Demonstrate Kubernetes self-healing by deleting Pods.
- Expose the application using a Kubernetes Service.
- Test the application using port forwarding.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python and Flask | Develop the web application |
| Docker | Build and run the application container |
| Kubernetes | Orchestrate and manage application Pods |
| Minikube | Run a local Kubernetes cluster |
| kubectl | Manage Kubernetes resources |
| YAML | Define Kubernetes configuration |
| VS Code | Development environment |

## 4. Project Structure

```text
Exercise-3/
├── app.py
├── Dockerfile
├── flashsale-replicaset.yaml
└── README.md
```

## 5. Application Endpoints

The Flask application provides the following endpoints:

| Endpoint | Description |
|---|---|
| `/` | Displays the application homepage |
| `/buy` | Simulates a product purchase |
| `/health` | Checks application health |

Example purchase request:

```text
http://localhost:8080/buy?user=123
```

The response contains the purchase status, product information, user ID, time, and the Pod that handled the request.

## 6. Implementation Steps

### Step 1: Build the Docker image

Build the Flask application image using the Dockerfile.

```bash
docker build -t flashsale:1.0 .
```

### Step 2: Load the image into Minikube

Load the locally built image into the Minikube environment.

```bash
minikube image load flashsale:1.0
```

### Step 3: Deploy the Kubernetes ReplicaSet

Apply the Kubernetes configuration file.

```bash
kubectl apply -f flashsale-replicaset.yaml
```

The YAML file defines a ReplicaSet named `flashsale-rs` and a Service named `flashsale-svc`.

The initial ReplicaSet configuration specifies 3 replicas.

### Step 4: Scale the application

Scale the ReplicaSet to 5 replicas.

```bash
kubectl scale rs flashsale-rs --replicas=5
```

Verify the number of replicas:

```bash
kubectl get rs flashsale-rs
```

Expected result:

```text
NAME           DESIRED   CURRENT   READY
flashsale-rs   5         5         5
```

### Step 5: Verify the Pods

List the application Pods:

```bash
kubectl get pods -l app=flashsale -o wide
```

The output should show 5 Pods with `1/1` Ready and `Running` status.

### Step 6: Test self-healing

Delete an application Pod:

```bash
kubectl delete pod <pod-name>
```

Replace `<pod-name>` with an actual Pod name returned by the previous command.

Check the Pods again:

```bash
kubectl get pods -l app=flashsale
```

The ReplicaSet detects that the number of Pods is below the desired count and creates a replacement Pod automatically.

### Step 7: Access the application

Forward local port 8080 to the Kubernetes Service.

```bash
kubectl port-forward service/flashsale-svc 8080:80
```

Keep the port-forward terminal running and open the following URL in a browser:

```text
http://localhost:8080
```

To test the purchase endpoint:

```text
http://localhost:8080/buy?user=123
```

## 7. Results and Observations

The following results were observed during execution:

1. The Docker image `flashsale:1.0` was built successfully.
2. The Flask application was deployed on Minikube.
3. The ReplicaSet was scaled to 5 replicas.
4. All 5 application Pods reached `1/1 Running` status.
5. When two Pods were manually deleted, Kubernetes created replacement Pods to maintain the desired replica count.
6. The Kubernetes Service exposed the application through port forwarding.
7. The purchase endpoint returned a successful response and identified the Pod that handled the request.

## 8. Conclusion

This exercise demonstrates the use of Kubernetes ReplicaSets for application scaling and self-healing. The ReplicaSet maintained 5 application replicas even after Pods were manually deleted.

The Kubernetes Service provided access to the Flask application, while Docker and Minikube enabled containerization and local Kubernetes deployment.

This exercise helped demonstrate basic container orchestration, replica management, scaling, and fault recovery using Kubernetes.
