pipeline {

    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                python -m venv %VENV_DIR%
                %VENV_DIR%\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                %VENV_DIR%\\Scripts\\activate
                pytest tests
                '''
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                echo Deploy step completed
                '''
            }
        }
    }
}
