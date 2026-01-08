pipeline {
    agent any

    environment {
        IMAGE_NAME = "chatbot-api"
        CONTAINER_NAME = "chatbot-api"
        APP_PORT = "8000"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh """
                    docker build -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage('Deploy Container') {
            steps {
                echo "Stopping old container (if exists)..."
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """

                echo "Running new container..."
                sh """
                    docker run -d \
                      --restart unless-stopped \
                      --name ${CONTAINER_NAME} \
                      -p ${APP_PORT}:${APP_PORT} \
                      ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Smoke Test') {
            steps {
                echo "Waiting for app to start..."
                sh "sleep 5"

                echo "Health check..."
                sh "curl -f http://localhost:${APP_PORT}/"
            }
        }
    }

    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
