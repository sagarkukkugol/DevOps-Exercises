# Exercise 7: Continuous Integration (CI) and Jenkins

## Objective

Learn the fundamentals of Continuous Integration (CI), understand Jenkins concepts, and create and run a simple Jenkins Pipeline.

## 1. Continuous Integration (CI)

Continuous Integration is a development practice where developers frequently integrate code changes into a shared repository. A CI server can build and test changes and provide feedback, helping teams detect problems early.

### Key features

- Frequent code integration
- Automated builds
- Automated testing
- Immediate feedback

### Benefits

- Earlier bug and integration issue detection
- Improved collaboration
- Faster development cycles
- Better software quality through automated checks

## 2. CI workflow

1. A developer commits and pushes code to a shared Git repository.
2. A CI server detects the change and starts a pipeline.
3. The pipeline builds the application and runs tests.
4. The CI server reports success or failure to the developer.

## 3. Jenkins concepts

- **Job/Project:** A task or process configured in Jenkins.
- **Build:** One execution of a Jenkins job.
- **Pipeline:** A sequence of stages and steps used to automate work.
- **Plugins:** Extensions that add Jenkins features.
- **Nodes:** Machines or environments where Jenkins jobs run.

## 4. Jenkins setup used

Jenkins was already running from the previous exercise, so the existing Jenkins instance was reused. No new Jenkins container was created.

Jenkins dashboard: http://localhost:8080/

## 5. Create the Exercise 7 pipeline job

1. Open `http://localhost:8080/` in your browser and sign in.
2. On the dashboard, click **New Item**.
3. Enter the item name: `Exercise-7-CI`.
4. Select **Pipeline**.
5. Click **OK**.
6. In the job configuration page, select **Pipeline** from the left-side menu or scroll to the Pipeline section.
7. Set **Definition** to **Pipeline script**.
8. Paste the pipeline script from the next section into the **Script** box.
9. Click **Save**.

## 6. Pipeline script

The following pipeline demonstrates four stages: Checkout, Build, Test, and Feedback.

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests'
            }
        }

        stage('Feedback') {
            steps {
                echo 'CI pipeline completed successfully'
            }
        }
    }
}
```

**Note:** This is a demonstration pipeline. Its stages print messages; they do not actually check out a repository, compile an application, or run a test suite.

## 7. Run the pipeline and inspect the result

1. Open the `Exercise-7-CI` job.
2. Click **Build Now**.
3. In the **Build History** area, click the new build number (for example, `#1`).
4. Click **Console Output**.
5. Check that the stages run and the final line says:

```text
Finished: SUCCESS
```

The successful run for this exercise showed the Checkout, Build, Test, and Feedback stages completing.

## 8. Troubleshooting

### Pipeline syntax error: unexpected token `}`

If Jenkins reports an error such as `unexpected token: }`, check the braces in the pipeline script. Replace the script with the complete version in Section 6, save, and run the job again.

### Build fails

Open the failed build number, then select **Console Output**. Read the first error message that appears before `Finished: FAILURE`. Correct that issue and run the job again.

## 9. GitHub: add the Exercise 7 README and push

These commands assume your local repository is `~/DevOps-Exercises`, your branch is `main`, and you downloaded this README into your Ubuntu **Downloads** folder.

1. Download `Exercise-7-README.md` from the ChatGPT attachment.
2. In Ubuntu Terminal, check that the downloaded file exists:

```bash
ls -l ~/Downloads/Exercise-7-README.md
```

3. Go to your repository and create the Exercise 7 folder if needed:

```bash
cd ~/DevOps-Exercises
mkdir -p Exercise-7
```

4. Copy the downloaded README into the project:

```bash
cp ~/Downloads/Exercise-7-README.md Exercise-7/README.md
```

5. Check the repository changes:

```bash
git status
```

6. Stage and commit the README:

```bash
git add Exercise-7/README.md
git commit -m "Add Exercise 7 CI Jenkins README"
```

7. Push the commit to GitHub:

```bash
git push origin main
```

8. Open your repository on GitHub and verify that `Exercise-7/README.md` appears.

Repository: https://github.com/sagarkukkugol/DevOps-Exercises

If the download is not in `~/Downloads`, find it with:

```bash
find ~/ -name "Exercise-7-README.md" 2>/dev/null
```

Use the path returned by `find` in the `cp` command.

## 10. Conclusion

This exercise introduced CI concepts and Jenkins terminology, demonstrated how to create and run a basic Jenkins Pipeline, and documented how to add the exercise README to the Git repository.
