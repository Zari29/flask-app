pipeline {

    agent any

    environment {
        APP_NAME = "flask_app"
        VENV_DIR = "venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-repo/flask-app.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                source $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate
                pytest tests --disable-warnings --maxfail=1
                '''
            }
        }

        stage('Build') {
            steps {
                echo "Build successful – Flask app ready"
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate

                # Kill previous app if running
                pkill -f gunicorn || true

                # Start Flask app using Gunicorn
                nohup gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app &
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Build & Deployment Successful"
        }
        failure {
            echo "❌ Build or Tests Failed"
        }
    }
}
