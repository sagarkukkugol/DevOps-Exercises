@"

\# Kubernetes Hands-On Exercise Series



Welcome to Exercise-1 \*\*Kubernetes (K8s) exercises\*\*!



These activities will help you understand the basics of how Kubernetes runs and manages containerized applications.



\## Business Problem (Zepto Example)



Imagine you are a \*\*DevOps Engineer at Zepto\*\*. The product team just built a lightweight \*\*web app\*\* that shows the \*\*storefront and delivery status page\*\* for customers.



Your task as the DevOps engineer:



\*\*Deploy this app on Kubernetes\*\* so that it is always running, portable, and can be scaled later. Simulate this using the popular `nginx` container image (think of it as Zepto's storefront web app).



\## Exercise 1: Hello Pod



\*\*Goal:\*\* Run your first app inside Kubernetes and access it.



\## Pre-Requisites



1\. \*\*Install Minikube (one-time setup)\*\*

&#x20;  - On Linux:

&#x20;    ```bash

&#x20;    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

&#x20;    sudo install minikube-linux-amd64 /usr/local/bin/minikube

&#x20;    ```



&#x20;  - On macOS (with Homebrew):

&#x20;    ```bash

&#x20;    brew install minikube

&#x20;    ```



&#x20;  - On Windows (PowerShell):

&#x20;    ```powershell

&#x20;    choco install minikube

&#x20;    ```



&#x20;  - On WSL:

&#x20;    ```bash

&#x20;    sudo apt-get update -y

&#x20;    sudo apt-get install -y curl apt-transport-https virtualbox virtualbox-ext-pack



&#x20;    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

&#x20;    sudo install minikube-linux-amd64 /usr/local/bin/minikube

&#x20;    ```



&#x20;  > You need \*\*Docker\*\* or a VM driver (VirtualBox, Hyper-V) installed.



\### Steps: Deploy Nginx Image as a Pod



1\. Start a local Kubernetes cluster with \*\*Minikube\*\*:

&#x20;  ```powershell

&#x20;  minikube start --driver=docker

