pipeline {
    agent any

    environment {
        APP_NAME = "online-shop"
        IMAGE_NAME = "online-shop:latest"
        CONTAINER_NAME = "online-shop-container"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/sivaprasadpappala/OnlineShopping.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 --version
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Static Code Check') {
            steps {
                sh '''
                . venv/bin/activate
                python -m py_compile app.py models.py
                '''
            }
        }

        stage('Initialize Database') {
            steps {
                sh '''
                . venv/bin/activate
                python db_init.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                docker rm -f ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Run Application Container') {
            steps {
                sh '''
                docker run -d \
                  --name ${CONTAINER_NAME} \
                  -p 5000:5000 \
                  ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo "Application deployed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}