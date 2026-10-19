# Exercise 6: Real-Time Operations Monitoring and Alerting

## Objective

To develop a real-time operations monitoring and alerting system for a delivery service using Python, Docker, Prometheus, Grafana, and Jenkins. The system collects delivery metrics, monitors application performance, visualizes the collected data, and generates alerts when predefined thresholds are exceeded.

## Technologies Used

- Python
- Prometheus Client
- Docker
- Prometheus
- Grafana
- Jenkins
- Git and GitHub

## Project Structure

```text
Exercise-6/
├── delivery_metrics.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── Jenkinsfile
└── prometheus/
    ├── prometheus.yml
    └── alert_rules.yml
```

## Step 1: Create a Python Application for Delivery Metrics

Create a Python application that simulates delivery activity and exposes metrics using the Prometheus Python client.

File Name: `delivery_metrics.py`

The application collects the following metrics:

- Total number of deliveries
- Number of pending deliveries
- Number of deliveries on the way
- Average delivery time

The metrics are exposed through an HTTP endpoint on port 8000.

```text
http://localhost:8000/metrics
```

This endpoint allows Prometheus to collect the delivery metrics at regular intervals.

## Step 2: Create the Requirements File

Create a file named `requirements.txt` to specify the Python dependency.

File Name: `requirements.txt`

```text
prometheus-client
```

Install the dependency using:

```bash
pip install -r requirements.txt
```

## Step 3: Create a Dockerfile for the Delivery Metrics Application

Create a Dockerfile to containerize the Python application and its dependencies.

File Name: `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY delivery_metrics.py .

EXPOSE 8000

CMD ["python", "delivery_metrics.py"]
```

## Step 4: Build and Run the Docker Image

Build the Docker image from the project directory.

```bash
docker build -t delivery-metrics .
```

Run the delivery metrics application as a container.

```bash
docker run -d \
  --name delivery-metrics \
  -p 8000:8000 \
  delivery-metrics
```

Verify that the container is running:

```bash
docker ps
```

Check whether the application is exposing metrics:

```bash
curl http://localhost:8000/metrics
```

The output should contain delivery metrics such as `total_deliveries`, `pending_deliveries`, and `average_delivery_time`.

## Step 5: Configure Prometheus for Metrics Collection

Create a Prometheus configuration file to collect metrics from the delivery metrics application.

File Name: `prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 5s

rule_files:
  - /etc/prometheus/alert_rules.yml

scrape_configs:
  - job_name: 'delivery-metrics'
    static_configs:
      - targets: ['172.17.0.1:8000']
```

The scrape interval is set to 5 seconds, meaning Prometheus attempts to collect metrics every 5 seconds.

The target address `172.17.0.1:8000` is the Docker host endpoint used in this Ubuntu setup. The target must be reachable from Prometheus.

Prometheus is accessed through:

```text
http://localhost:9090
```

Check the Prometheus target status through:

```text
Status → Targets
```

The delivery metrics target should display **UP** when collection is successful.

## Step 6: Configure Prometheus Alert Rules

Create alert rules to detect abnormal delivery operations.

File Name: `prometheus/alert_rules.yml`

### Alert 1: High Pending Deliveries

This alert is triggered when pending deliveries exceed 10 for 15 seconds.

```yaml
- alert: HighPendingDeliveries
  expr: pending_deliveries > 10
  for: 15s
  labels:
    severity: warning
  annotations:
    summary: High number of pending deliveries
    description: Pending deliveries have exceeded 10 for 15 seconds.
```

### Alert 2: High Average Delivery Time

This alert is triggered when the average delivery time exceeds 30 seconds for 15 seconds.

```yaml
- alert: HighAverageDeliveryTime
  expr: average_delivery_time_sum / average_delivery_time_count > 30
  for: 15s
  labels:
    severity: critical
  annotations:
    summary: High average delivery time
    description: Average delivery time has exceeded 30 seconds for 15 seconds.
```

The alerts help identify delivery delays and high pending delivery counts.

## Step 7: Create a Grafana Dashboard

Grafana is used to visualize the metrics collected by Prometheus.

Access Grafana through:

```text
http://localhost:3000
```

Configure Prometheus as the data source and create a dashboard named:

**Delivery Monitoring**

The dashboard can display:

- Total deliveries
- Pending deliveries
- Deliveries on the way
- Average delivery time

The dashboard provides a visual overview of delivery operations and helps identify changes in delivery activity.

## Step 8: Configure Jenkins for Pipeline Execution

Jenkins is configured to execute a pipeline that checks Docker and monitoring connectivity.

File Name: `Jenkinsfile`

```groovy
pipeline {
    agent any

    stages {
        stage('Start') {
            steps {
                echo 'Starting Exercise 6: Delivery Monitoring'
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker --version'
                sh 'docker ps'
            }
        }

        stage('Check Monitoring') {
            steps {
                sh 'curl -f http://172.17.0.1:8000/metrics'
            }
        }
    }
}
```

The pipeline contains three stages:

1. **Start:** Displays the pipeline start message.
2. **Check Docker:** Verifies Docker availability and lists running containers.
3. **Check Monitoring:** Requests the delivery metrics endpoint and checks whether it responds successfully.

Jenkins retrieves the pipeline script from the GitHub repository.

## Step 9: Configure GitHub Integration

The project is stored in the following GitHub repository:

[DevOps-Exercises](https://github.com/sagarkukkugol/DevOps-Exercises)

Jenkins is configured with:

- Repository URL: `https://github.com/sagarkukkugol/DevOps-Exercises.git`
- Branch: `main`
- Script Path: `Exercise-6/Jenkinsfile`

Jenkins checks out the repository and executes the pipeline defined in the Jenkinsfile.

## Step 10: Verify the Complete Monitoring System

The following commands and interfaces are used to verify the system.

### Verify Docker Containers

```bash
docker ps
```

Confirm that the delivery metrics application, Prometheus, Grafana, and Jenkins containers are running.

### Verify Application Metrics

```bash
curl http://localhost:8000/metrics
```

Confirm that delivery metrics are available.

### Verify Prometheus

Open:

```text
http://localhost:9090
```

Confirm that the delivery metrics target is UP and that the alert rules are loaded.

### Verify Grafana

Open:

```text
http://localhost:3000
```

Confirm that the Delivery Monitoring dashboard is available.

### Verify Jenkins

Open:

```text
http://localhost:8080
```

Run the pipeline and check the Console Output.

The pipeline should finish with:

```text
Finished: SUCCESS
```

## Result

The real-time operations monitoring and alerting system was successfully implemented.

The Python application generates delivery metrics, Docker runs the application, Prometheus collects and evaluates the metrics, Grafana visualizes the monitoring data, and Jenkins verifies Docker and monitoring connectivity through a pipeline.

The project demonstrates real-time application monitoring, threshold-based alerting, containerization, and CI pipeline execution.
