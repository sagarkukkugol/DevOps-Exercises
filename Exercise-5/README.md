# Exercise 5: Docker Security with AppArmor

## Objective
Secure a Flask application running inside a Docker container
using a custom AppArmor security profile.

## Technologies
- Python
- Flask
- Docker
- AppArmor
- Docker SDK for Python

## Features
- Flask application running inside Docker
- Custom AppArmor profile
- Restricted access to /etc/passwd
- Python automation to build and run the container

## Verification
- Flask application responds successfully
- Custom AppArmor profile is active
- Access to /etc/passwd is denied

## Run the application
docker build -t flask-apparmor .
docker run -d --name flask-secure --security-opt apparmor=flask-apparmor-profile -p 5000:5000 flask-apparmor

## Test
curl http://localhost:5000/
