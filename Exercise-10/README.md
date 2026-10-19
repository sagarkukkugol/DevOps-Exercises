# Exercise 10: Multi-Node Kubernetes Cluster with Multiple Applications

## Objective

Deploy two Flask applications to a three-node Kubernetes cluster and verify that their replicas are distributed across the nodes.

- **AppA — Product Catalog:** 2 replicas
- **AppB — Shopping Cart:** 3 replicas
- Expose both applications through Kubernetes `NodePort` Services.
- Test the applications using HTTP requests.

## Environment

- Ubuntu running in VirtualBox
- Minikube with the Docker driver
- Kubernetes v1.37.0
- Minikube profile: `devops-multinode`
- Three nodes:
  - `devops-multinode` (control plane)
  - `devops-multinode-m02`
  - `devops-multinode-m03`

> Commands below assume the project files are in `~/Exercise-10`. Run Kubernetes commands with the `devops-multinode` profile.

## Architecture

```text
                         Minikube profile: devops-multinode
                  ┌───────────────────────────────────────────┐
                  │          Kubernetes cluster             │
                  │                                       │
                  │  Node: devops-multinode (control plane)│
                  │       └── Shopping Cart pod (1)        │
                  │                                       │
                  │  Node: devops-multinode-m02            │
                  │       ├── Product Catalog pod (1)      │
                  │       └── Shopping Cart pod (1)        │
                  │                                       │
                  │  Node: devops-multinode-m03            │
                  │       ├── Product Catalog pod (1)      │
                  │       └── Shopping Cart pod (1)        │
                  └───────────────────────────────────────────┘

  Product Catalog NodePort: 32528  -> Service port 80 -> Pods port 80
  Shopping Cart NodePort:   32637  -> Service port 80 -> Pods port 80
```

## 1. Create the three-node Minikube cluster

The cluster used for this exercise was named `devops-multinode`.

```bash
minikube start -p devops-multinode --nodes 3 --driver=docker
```

Check the nodes:

```bash
minikube -p devops-multinode kubectl -- get nodes -o wide
```

All three nodes should show `Ready`.

## 2. Build the application container images

The project contains two Flask applications and separate Dockerfiles:

- `product_catalog.py` — Product Catalog endpoint at `/products`
- `shopping_cart.py` — Shopping Cart endpoints at `/cart`
- `Dockerfile.product`
- `Dockerfile.shopping`

Build the images from the project directory:

```bash
cd ~/Exercise-10

docker build -f Dockerfile.product -t product-catalog:latest .
docker build -f Dockerfile.shopping -t shopping-cart:latest .
```

Load the images into the Minikube cluster so the pods can use them:

```bash
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

The deployments use `imagePullPolicy: Never`, so Kubernetes uses the images loaded into the cluster rather than trying to pull them from a remote registry.

## 3. Product Catalog Deployment (AppA)

Create `product-deployment.yaml` with a Deployment configured for **2 replicas**. The pod template uses the label `app: product-catalog` and the container image `product-catalog:latest`.

The deployment uses required pod anti-affinity with the topology key `kubernetes.io/hostname`, so the two Product Catalog replicas are scheduled on different nodes.

Apply it:

```bash
minikube -p devops-multinode kubectl -- apply -f product-deployment.yaml
```

## 4. Product Catalog Service

Create `product-service.yaml` as a `NodePort` Service:

- Service name: `product-service`
- Selector: `app: product-catalog`
- Service port: `80`
- Target port: `80`

Apply it:

```bash
minikube -p devops-multinode kubectl -- apply -f product-service.yaml
```

## 5. Shopping Cart Deployment (AppB)

Create `shopping-deployment.yaml` with a Deployment configured for **3 replicas**. The pod template uses the label `app: shopping-cart` and the container image `shopping-cart:latest`.

Required pod anti-affinity with topology key `kubernetes.io/hostname` spreads the three Shopping Cart replicas across the three nodes.

Apply it:

```bash
minikube -p devops-multinode kubectl -- apply -f shopping-deployment.yaml
```

## 6. Shopping Cart Service

Create `shopping-service.yaml` as a `NodePort` Service:

- Service name: `shopping-service`
- Selector: `app: shopping-cart`
- Service port: `80`
- Target port: `80`

Apply it:

```bash
minikube -p devops-multinode kubectl -- apply -f shopping-service.yaml
```

## 7. Verify the cluster and deployments

Check nodes:

```bash
minikube -p devops-multinode kubectl -- get nodes -o wide
```

Check deployments:

```bash
minikube -p devops-multinode kubectl -- get deployments
```

Expected deployment result:

```text
NAME              READY   UP-TO-DATE   AVAILABLE
product-catalog   2/2     2            2
shopping-cart     3/3     3            3
```

Check pods and their node placement:

```bash
minikube -p devops-multinode kubectl -- get pods -o wide
```

Observed successful output (pod suffixes and ages can change):

```text
NAME                              READY   STATUS    RESTARTS   AGE     IP           NODE
product-catalog-fc7b5ff55-75nnp   1/1     Running   0          6m4s    10.244.2.4   devops-multinode-m03
product-catalog-fc7b5ff55-jr7hk   1/1     Running   0          6m4s    10.244.1.3   devops-multinode-m02
shopping-cart-68655875d6-25pfb    1/1     Running   0          4m44s   10.244.1.4   devops-multinode-m02
shopping-cart-68655875d6-bkd6g    1/1     Running   0          4m44s   10.244.2.5   devops-multinode-m03
shopping-cart-68655875d6-p6l5r    1/1     Running   0          4m43s   10.244.0.4   devops-multinode
```

Check Services:

```bash
minikube -p devops-multinode kubectl -- get services
```

Observed successful output:

```text
NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)
kubernetes          ClusterIP  10.96.0.1        <none>        443/TCP
product-service     NodePort    10.98.181.63     <none>        80:32528/TCP
shopping-service    NodePort    10.109.246.160   <none>        80:32637/TCP
```

## 8. Test the applications

Get the Minikube IP:

```bash
minikube -p devops-multinode ip
```

For this run, the IP was:

```text
192.168.58.2
```

### Product Catalog GET request

```bash
curl http://192.168.58.2:32528/products
```

Observed response:

```json
[{"id":1,"name":"Laptop"},{"id":2,"name":"Phone"},{"id":3,"name":"Headphones"}]
```

### Shopping Cart GET request (initially empty)

```bash
curl http://192.168.58.2:32637/cart
```

Observed response:

```json
[]
```

### Add a product to the cart (POST)

```bash
curl -X POST http://192.168.58.2:32637/cart \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "name": "Laptop"}'
```

Observed response:

```json
{"cart":[{"name":"Laptop","product_id":1}],"message":"Item added"}
```

### Verify the cart (GET)

```bash
curl http://192.168.58.2:32637/cart
```

Observed response:

```json
[{"name":"Laptop","product_id":1}]
```

## 9. Final result

The exercise was verified successfully:

- Three Kubernetes nodes were Ready.
- Product Catalog had **2/2 available replicas**.
- Shopping Cart had **3/3 available replicas**.
- All five application pods were Running with zero restarts in the final check.
- Product Catalog and Shopping Cart replicas were distributed across the three nodes.
- Both NodePort Services were created.
- Product Catalog GET and Shopping Cart GET/POST requests returned the expected responses.

## Notes

- The Minikube IP and generated pod names can change in a later cluster run. Use `minikube -p devops-multinode ip` and `kubectl get pods -o wide` to check current values.
- The Shopping Cart app stores its cart in application memory in this exercise. Cart contents may be lost if the pod restarts; persistent storage was not configured.
- If you rebuild an image, load it into the Minikube profile again before restarting/recreating pods.
