# Exercise 9: Jenkins Multi-Stage Pipeline for Python Flask Application

## Objective

The objective of this exercise is to create and execute a multi-stage Jenkins pipeline to automate the build, testing, deployment, and execution of a Python Flask application.

The pipeline demonstrates how Jenkins can automate the software delivery process using a Jenkinsfile.

## Technologies Used

- Jenkins – CI/CD pipeline automation
- Docker – Running Jenkins in a container
- Python – Application development
- Flask – Web application framework
- Git and GitHub – Source code management
- Linux – Execution environment

## Project Structure

```text
Exercise-9/
└── python-flask-app/
    ├── app.py
    ├── requirements.txt
    ├── test_app.py
    └── Jenkinsfile
```

## Application Description

The Flask application provides a simple home page.

When the application is running, accessing the following URL:

http://localhost:5000

returns:

```text
Hello, Jenkins Multi-Stage Pipeline!
```

## Pipeline Stages

The Jenkins pipeline consists of six stages.

### 1. Build

This stage prepares the Python application environment.

Tasks performed:

- Create a Python virtual environment.
- Install the required Python dependencies from `requirements.txt`.
- Prepare the application for testing and execution.

### 2. Test

This stage executes the application's automated unit tests.

The test script `test_app.py` verifies:

- The Flask application responds successfully.
- The home page returns HTTP status code 200.
- The response contains the expected message.

The pipeline continues only if the tests pass.

### 3. Deploy

This stage prepares the application for deployment.

Tasks performed:

- Create the deployment directory.
- Copy `app.py` into the deployment directory.
- Prepare the application files for execution.

Deployment directory:

```text
python-app-deploy/
```

### 4. Run Application

This stage starts the Flask application.

Tasks performed:

- Execute the deployed application using the Python virtual environment.
- Run the application in the background.
- Store the process ID and application logs.

The Flask application listens on port 5000.

### 5. Test Application

This stage verifies that the deployed application is running correctly.

Tasks performed:

- Send an HTTP request to the application.
- Verify that the application responds successfully.
- Check that the expected response message is returned.

Expected response:

```text
Hello, Jenkins Multi-Stage Pipeline!
```

### 6. Pipeline Completion

If all the previous stages succeed, Jenkins marks the pipeline as successful.

Expected result:

```text
Finished: SUCCESS
```

## Jenkins Configuration

### Step 1: Create a Jenkins Pipeline Job

1. Open Jenkins at:

   http://localhost:8080

2. Click **New Item**.
3. Enter the job name:

   `Python-MultiStage-Pipeline`

4. Select **Pipeline**.
5. Click **OK**.

### Step 2: Configure GitHub Repository

Under the Pipeline section, select:

`Pipeline script from SCM`

Configure the following:

| Setting | Value |
|---|---|
| SCM | Git |
| Repository URL | `https://github.com/sagarkukkugol/DevOps-Exercises.git` |
| Branch | `*/main` |
| Script Path | `Exercise-9/python-flask-app/Jenkinsfile` |

Save the configuration.

### Step 3: Execute the Pipeline

1. Open the `Python-MultiStage-Pipeline` job.
2. Click **Build Now**.
3. Open the latest build.
4. Click **Console Output**.
5. Observe the execution of all pipeline stages.

## Expected Output

The pipeline should complete the following operations successfully:

- Python virtual environment creation.
- Dependency installation.
- Unit test execution.
- Application deployment.
- Flask application startup.
- HTTP response verification.

The final Jenkins build status should be:

```text
SUCCESS
```

The application should return:

```text
Hello, Jenkins Multi-Stage Pipeline!
```

## Conclusion

In this exercise, a multi-stage Jenkins pipeline was successfully created and executed for a Python Flask application.

The pipeline automates the build, test, deployment, and application verification processes.

This exercise demonstrates how Jenkins can be used to automate repetitive software development tasks and improve the reliability of application delivery.
```
