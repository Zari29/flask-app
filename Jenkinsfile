pipeline {
    agent any

    // ---------- PARAMETERS ----------
    parameters {
        booleanParam(
            name: 'executeTests',
            defaultValue: true,
            description: 'Run the Test stage?'
        )
    }

    // ---------- ENVIRONMENT VARIABLES ----------
    environment {
        VERSION = "1.0.1"
        APP_NAME = "FlaskAppFinal"
        VENV = "${WORKSPACE}\\venv"
        SONAR_TOKEN = credentials('sonarcloud-token') // Use the token you stored in Jenkins Credentials
    }

    stages {

        // ---------- SETUP ----------
        stage('Setup') {
            steps {
                echo "Setting up Python environment..."
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate.bat && pip install --upgrade pip'
                bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                echo "Environment setup completed."
            }
        }

        // ---------- TEST ----------
        stage('Test') {
            when {
                expression { return params.executeTests == true }
            }
            steps {
                echo "Running tests..."
                bat 'venv\\Scripts\\activate.bat && pytest tests\\ --junitxml=report.xml'
                echo "Tests completed."
            }
        }

        // ---------- SONARCLOUD SCAN ----------
        stage('SonarCloud Analysis') {
            steps {
                echo "Running SonarCloud analysis..."
                bat """
                set SONAR_TOKEN=${SONAR_TOKEN}
                venv\\Scripts\\activate.bat
                sonar-scanner ^
                  -Dsonar.organization=your_org_key ^
                  -Dsonar.projectKey=your_project_key ^
                  -Dsonar.sources=. ^
                  -Dsonar.host.url=https://sonarcloud.io ^
                  -Dsonar.login=%SONAR_TOKEN%
                """
                echo "SonarCloud scan completed."
            }
        }

        // ---------- DEPLOY (Optional) ----------
        stage('Deploy') {
            steps {
                echo "Deploying ${APP_NAME} version ${VERSION}..."
                // Example: run Flask locally for testing
                bat 'venv\\Scripts\\activate.bat && set FLASK_APP=server.py && flask run --host=0.0.0.0 --port=5000'
            }
        }
    }

    // ---------- POST-BUILD ACTIONS ----------
    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
        always {
            echo "Pipeline finished (success or fail)."
        }
    }
}
