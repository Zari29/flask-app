pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'executeTests',
            defaultValue: true,
            description: 'Run the Test stage?'
        )
    }

    environment {
        VERSION = "1.0.1"
        APP_NAME = "FlaskAppFinal"
        VENV = "${WORKSPACE}\\venv"
        SONAR_TOKEN = credentials('sonarcloud-token') // Jenkins Secret Text
        SONAR_SCANNER = "C:\\sonar-scanner\\bin\\sonar-scanner.bat" // Update path if needed
    }

    stages {

        stage('Setup') {
            steps {
                echo "Setting up Python environment..."
                bat 'python -m venv venv'
                bat "${VENV}\\Scripts\\pip.exe install --upgrade pip"
                bat "${VENV}\\Scripts\\pip.exe install -r requirements.txt"
                echo "Python environment setup completed."
            }
        }

        stage('Test') {
            when {
                expression { return params.executeTests == true }
            }
            steps {
                echo "Running tests..."
                bat "${VENV}\\Scripts\\pytest.exe tests\\ --junitxml=report.xml"
                echo "Tests completed."
            }
        }

        stage('SonarCloud Analysis') {
            steps {
                echo "Running SonarCloud analysis..."
                bat "\"${SONAR_SCANNER}\" -Dsonar.organization=flaskapp -Dsonar.projectKey=flaskapp_flask -Dsonar.sources=. -Dsonar.host.url=https://sonarcloud.io -Dsonar.login=%SONAR_TOKEN%"
                echo "SonarCloud scan completed."
            }
        }

        stage('Deploy (Optional)') {
            steps {
                echo "Starting Flask app in background..."
                bat 'start cmd /c "${VENV}\\Scripts\\python.exe -m flask run --host=0.0.0.0 --port=5000"'
                echo "Flask started in background."
            }
        }
    }

    post {
        success { echo "Pipeline completed successfully!" }
        failure { echo "Pipeline failed!" }
        always { echo "Pipeline finished (success or fail)." }
    }
}
