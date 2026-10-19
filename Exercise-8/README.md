# Exercise 8: Jenkins Hello World

## Objective
Create a shell script and execute it using a Jenkins Freestyle project.

## Source Code
The `hello-world.sh` script prints the message:

Hello, Jenkins!

## Jenkins Configuration
- Job Name: HelloWorld
- Project Type: Freestyle Project
- Source Code Management: Git
- Repository: https://github.com/sagarkukkugol/DevOps-Exercises.git
- Build Step: Execute Shell

## Shell Commands
```bash
cd Exercise-8
chmod +x hello-world.sh
./hello-world.sh
