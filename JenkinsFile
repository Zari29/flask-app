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
        VERSION = "1.0.0"
        APP_NAME = "FlaskApp"
    }

    // ---------- TOOLS ----------
    tools {
        // Make sure this name matches Jenkins → Manage Jenkins → Tools → Maven
        maven 'MAVEN'
    }

    stages {

        // ---------- BUILD ----------
        stage('Build') {
            steps {
                echo "Building ${APP_NAME} version ${VERSION}"
                sh 'mvn --version'     // Windows = bat 'mvn --version'
                echo "Build completed."
            }
        }

        // ---------- TEST ----------
        stage('Test') {
            when {
                expression { return params.executeTests == true }
            }
            steps {
                echo "Running tests..."
                echo "Tests completed."
            }
        }

        // ---------- DEPLOY ----------
        stage('Deploy') {
            steps {
                echo "Deploying application..."
                echo "Deployment done!"
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
