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
        SONAR_TOKEN = credentials('sonarcloud-token') // Your Jenkins secret text ID
        SONAR_SCANNER = "C:\\sonar-scanner\\bin\\sonar-scanner.bat" // Update path if needed
    }

    stages {

        // ---------- SETUP ----------
        stage('Setup') {
            steps {
                echo "Setting up Python environment..."
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate.bat && pip install --upgrade pip'
                bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                echo "Python environment setup completed."
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
                "${SONAR_SCANNER}" ^
                  -Dsonar.organization=flaskapp ^
                  -Dsonar.projectKey=flaskapp_flask ^
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
                echo "Starting Flask app in background..."
                // Runs Flask in a separate cmd window so Jenkins pipeline continues
                bat 'start cmd /c "venv\\Scripts\\activate.bat && set FLASK_APP=app.py && flask run --host=0.0.0.0 --port=5000"'
                echo "Flask started in background."
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
