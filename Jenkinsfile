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
        VENV = "${WORKSPACE}\\venv"
        SONAR_TOKEN = credentials('sonarcloud-token')
        SONAR_SCANNER = "C:\\sonar-scanner\\bin\\sonar-scanner.bat"
    }

    stages {

        stage('Setup') {
            steps {
                bat 'python -m venv venv'
                bat "${VENV}\\Scripts\\pip.exe install -r requirements.txt"
            }
        }

        stage('Initialize Database') {
            steps {
                bat """
                ${VENV}\\Scripts\\python.exe -c "from app import db, app; app.app_context().push(); db.create_all()"
                """
            }
        }

        stage('PyTest Unit Tests') {
            when {
                expression { params.executeTests }
            }
            steps {
                bat "${VENV}\\Scripts\\pytest.exe tests\\ --junitxml=report.xml"
            }
        }

        stage('Deploy Flask App') {
            steps {
                bat """
                set FLASK_APP=app.py
                start cmd /c "${VENV}\\Scripts\\python.exe -m flask run --host=0.0.0.0 --port=5000"
                """
            }
        }

        stage('TestNG Smoke Tests') {
            steps {
                bat "mvn test -DsuiteXmlFile=testng.xml"
            }
        }
    }

    post {
        success { echo "CI/CD Pipeline executed successfully!" }
        failure { echo "Pipeline failed!" }
    }
}
