# Exercise 5: Docker Security with AppArmor

## 1. Overview

This exercise demonstrates how to secure a Python Flask web application running inside a Docker container using a custom AppArmor security profile.

AppArmor is a Linux security module that restricts the capabilities and resources available to applications through profile-based access control. In this exercise, a custom profile is applied to the Flask container to restrict access to sensitive files and system resources.

The application is also managed using the Docker SDK for Python, which automates the process of building the Docker image, starting the container with the AppArmor profile, verifying the active security profile, and cleaning up the container.

## 2. Objectives

- Run a Flask web application inside a Docker container.
- Create and configure a custom AppArmor security profile.
- Restrict access to sensitive files such as `/etc/passwd`.
- Apply the AppArmor profile to a Docker container.
- Automate Docker operations using the Docker SDK for Python.
- Verify application functionality and security restrictions.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development and automation |
| Flask | Web application framework |
| Docker | Containerization |
| AppArmor | Linux application security |
| Docker SDK for Python | Automating Docker operations |
| Ubuntu | Linux environment for AppArmor |

## 4. Project Structure

```text
Exercise-5/
├── app.py
├── Dockerfile
├── requirements.txt
├── apply_apparmor.py
├── flask-apparmor-profile
└── README.md
```

## 5. Application Description

The Flask application provides a simple web endpoint that returns a greeting message when accessed.

The application runs on port 5000 and listens on all available network interfaces inside the container.

The custom AppArmor profile is used to restrict the application's access to selected files and system resources.

## 6. Installation and Setup

### Step 1: Install Docker

Install Docker Engine on Ubuntu and verify the installation.

```bash
docker --version
```

### Step 2: Install AppArmor

Install the required AppArmor utilities.

```bash
sudo apt install apparmor apparmor-utils -y
```

Verify AppArmor status:

```bash
sudo aa-status
```

### Step 3: Install Python Dependencies

Create and activate a Python virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages.

```bash
pip install flask docker
```

Alternatively, install dependencies from the requirements file:

```bash
pip install -r requirements.txt
```

## 7. Build the Docker Image

Navigate to the Exercise-5 directory containing the Dockerfile.

Build the Docker image:

```bash
docker build -t flask-apparmor .
```

Verify the image:

```bash
docker images
```

## 8. Configure the AppArmor Profile

Create the custom AppArmor profile at:

```text
/etc/apparmor.d/flask-apparmor-profile
```

Load or update the profile:

```bash
sudo apparmor_parser -r /etc/apparmor.d/flask-apparmor-profile
```

Verify that the profile is loaded:

```bash
sudo aa-status
```

The profile should appear in the list of loaded AppArmor profiles.

## 9. Run the Application

Start the Flask application inside a Docker container with the custom AppArmor profile.

```bash
docker run -d \
  --name flask-secure \
  --security-opt apparmor=flask-apparmor-profile \
  -p 5000:5000 \
  flask-apparmor
```

Check the running container:

```bash
docker ps
```

View application logs:

```bash
docker logs flask-secure
```

## 10. Test the Application

Access the Flask application using curl:

```bash
curl http://localhost:5000/
```

Expected response:

```text
Hello, this is a secure Flask application running inside a Docker container!
```

## 11. Security Verification

### Verify the active AppArmor profile

```bash
docker inspect flask-secure --format '{{.AppArmorProfile}}'
```

Expected output:

```text
flask-apparmor-profile
```

### Verify restricted file access

Attempt to read `/etc/passwd` from inside the container:

```bash
docker exec flask-secure python -c "open('/etc/passwd').read()"
```

Expected result:

```text
PermissionError: [Errno 13] Permission denied: '/etc/passwd'
```

This confirms that access to the protected file is denied under the configured AppArmor policy.

## 12. Python Automation

The `apply_apparmor.py` script automates the Docker operations using the Docker SDK for Python.

The script performs the following operations:

1. Connects to the Docker daemon.
2. Builds the Flask Docker image.
3. Starts a container using the custom AppArmor profile.
4. Inspects the container to verify the active profile.
5. Stops and removes the container.

Run the automation script:

```bash
python apply_apparmor.py
```

## 13. Cleanup

Stop the running container:

```bash
docker stop flask-secure
```

Remove the container:

```bash
docker rm flask-secure
```

The Docker image can be retained for future testing.

## 14. Conclusion

This exercise demonstrates the use of Docker and AppArmor to improve the security of a Flask web application.

The application was successfully containerized and executed with a custom AppArmor profile. Security verification confirmed that the intended profile was active and that access to `/etc/passwd` was denied.

The Python Docker SDK was also used to automate image building, container execution, profile verification, and cleanup.

The exercise highlights the importance of applying security restrictions to containerized applications and verifying that those restrictions work as intended.
