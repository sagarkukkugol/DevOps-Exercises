# Exercise 6: Real-Time Operations Monitoring and Alerting

## 1. Introduction

In this exercise, a real-time operations monitoring and alerting system is developed for a delivery service. The system collects delivery-related metrics, monitors application performance, visualizes the collected data, and generates alerts when predefined conditions are met.

The project uses Python to generate delivery metrics, Docker to containerize the application, Prometheus to collect and evaluate metrics, Grafana to visualize monitoring data, and Jenkins to automate pipeline execution.

## 2. Objective

The main objectives of this exercise are:

- Develop a Python application that generates delivery metrics.
- Containerize the application using Docker.
- Collect application metrics using Prometheus.
- Create a Grafana dashboard to visualize delivery metrics.
- Configure Prometheus alert rules for delivery-related conditions.
- Create a Jenkins pipeline to verify Docker and monitoring connectivity.
- Store the project and Jenkins pipeline in GitHub.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Generate delivery metrics |
| Prometheus Client | Expose application metrics |
| Docker | Containerize the Python application |
| Prometheus | Collect metrics and evaluate alert rules |
| Grafana | Visualize monitoring metrics |
| Jenkins | Execute the CI pipeline |
| Git and GitHub | Version control and source code storage |

## 4. Project Structure

```text
Exercise-6/
│
├── delivery_metrics.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── Jenkinsfile
├── README.md
│
└── prometheus/
    ├── prometheus.yml
    └── alert_rules.yml
```

## 5. Implementation

### Step 1: Develop the Delivery Metrics Application

A Python application named `delivery_metrics.py` is developed using the Prometheus Python client.

The application simulates delivery activity and exposes the following metrics:

| Metric | Description |
|---|---|
| `total_deliveries` | Total number of deliveries |
| `pending_deliveries` | Number of pending deliveries |
| `on_the_way_deliveries` | Number of deliveries currently on the way |
| `average_delivery_time` | Delivery time observations in seconds |

The application starts a metrics HTTP server on port 8000.

Metrics can be accessed through:

```text
http://localhost:8000/metrics
```

### Step 2: Configure Python Dependencies

The `requirements.txt` file contains the Prometheus client dependency.

```text
prometheus-client
```

The Python application is executed in a virtual environment during development.

### Step 3: Containerize the Application

A Dockerfile is created to package the Python application and its dependencies into a Docker image.

The Docker image is built using:

```bash
docker build -t delivery-metrics .
```

The application container is started using:

```bash
docker run -d \
  --name delivery-metrics \
  -p 8000:8000 \
  delivery-metrics
```

The container exposes port 8000 to make the application metrics accessible.

### Step 4: Configure Prometheus

Prometheus is configured to scrape metrics from the delivery metrics application.

The Prometheus configuration file is located at:

```text
prometheus/prometheus.yml
```

The configuration defines the scrape interval and the target application endpoint.

Prometheus is accessed through:

```text
http://localhost:9090
```

The application target is verified through the Prometheus Targets page. The delivery metrics target should display an UP status when Prometheus can successfully collect metrics.

### Step 5: Configure Alert Rules

Prometheus alert rules are defined in:

```text
prometheus/alert_rules.yml
```

The project contains the following alerts:

#### HighPendingDeliveries

This alert is triggered when the number of pending deliveries exceeds 10 for 15 seconds.

```promql
pending_deliveries > 10
```

Severity: Warning

#### HighAverageDeliveryTime

This alert is triggered when the average delivery time exceeds 30 seconds for 15 seconds.

```promql
average_delivery_time_sum / average_delivery_time_count > 30
```

Severity: Critical

The alert rules are validated using Prometheus rule validation tools.

### Step 6: Configure Grafana

Grafana is used to visualize the delivery metrics collected by Prometheus.

Grafana is accessed through:

```text
http://localhost:3000
```

The Prometheus data source is configured to connect to the Prometheus server.

A dashboard named **Delivery Monitoring** is created to monitor the delivery metrics.

The dashboard helps observe:

- Total deliveries
- Pending deliveries
- Deliveries on the way
- Average delivery time

### Step 7: Configure Jenkins

Jenkins is used to execute the delivery monitoring verification pipeline.

The Jenkins installation is configured with Docker CLI and access to the Docker engine running on the Ubuntu host.

The Jenkins pipeline is stored in:

```text
Exercise-6/Jenkinsfile
```

The pipeline contains the following stages:

1. **Start** – Displays the start message for the monitoring pipeline.
2. **Check Docker** – Verifies Docker availability and lists running containers.
3. **Check Monitoring** – Requests the delivery metrics endpoint and verifies that it responds successfully.

The pipeline is configured to retrieve its script from the GitHub repository.

### Step 8: GitHub Integration

The project is stored in the following repository:

[DevOps-Exercises](https://github.com/sagarkukkugol/DevOps-Exercises)

The Jenkins pipeline is configured with:

- Repository: `https://github.com/sagarkukkugol/DevOps-Exercises.git`
- Branch: `main`
- Script Path: `Exercise-6/Jenkinsfile`

Jenkins retrieves the pipeline script from GitHub and executes the defined stages.

## 6. System Architecture

```text
                 Delivery Metrics Application
                          |
                          v
                    Python Client
                          |
                          v
                  Docker Container
                          |
                          v
                  Metrics Endpoint
                    Port 8000
                          |
                          v
                     Prometheus
                    Port 9090
                     /      \
                    v        v
              Alert Rules  Grafana
                           Port 3000
                              |
                              v
                    Delivery Monitoring
                         Dashboard


                     Jenkins Pipeline
                            |
                            v
                    GitHub Repository
                            |
                            v
                 Docker and Metrics Checks
```

## 7. Verification and Results

The following results were verified during execution:

- The Python delivery metrics application successfully exposed metrics.
- The Docker container for the delivery metrics application was running.
- Prometheus successfully collected metrics from the application.
- The Prometheus delivery metrics target was verified as UP.
- Both delivery alert rules were verified in the FIRING state during testing.
- Grafana was running and the Delivery Monitoring dashboard was created.
- Jenkins successfully accessed the Docker engine.
- Jenkins retrieved `Exercise-6/Jenkinsfile` from GitHub.
- All three Jenkins pipeline stages completed successfully.

The final Jenkins pipeline result was:

```text
Finished: SUCCESS
```

## 8. Conclusion

The Real-Time Operations Monitoring and Alerting exercise was successfully implemented using Python, Docker, Prometheus, Grafana, Jenkins, and GitHub.

The project demonstrates application metrics collection, containerized monitoring, dashboard visualization, threshold-based alerting, and CI pipeline verification.

The completed system provides a foundation for observing delivery operations and identifying situations such as high pending deliveries and increased average delivery time.
