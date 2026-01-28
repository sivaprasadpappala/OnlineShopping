pipeline {
    agent any

    environment {
        IMAGE_NAME = "sivaprasadpappala/online-shop"
        K8S_NAMESPACE = "default"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
        GITOPS_REPO = "https://github.com/sivaprasadpappala/OnlineShoppingGitops.git"
        GITOPS_DIR  = "gitops"
    }

    stages {

        stage('Checkout source') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Python Security Scan (Bandit)') {
            steps {
                sh '''
                . venv/bin/activate
                bandit -r . -f json -o bandit-report.json || true
                '''
            }
        }

        stage('SonarQube Scan') {
            environment {
                SONAR_SCANNER_HOME = tool 'SonarQubeScanner'
            }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    ${SONAR_SCANNER_HOME}/bin/sonar-scanner
                    '''
                }
            }
        }

        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                trivy image --severity CRITICAL \
                  --exit-code 1 \
                  --ignore-unfixed \
                  ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Update GitOps Repo') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                    git clone https://${GIT_USER}:${GIT_TOKEN}@https://github.com/sivaprasadpappala/OnlineShoppingGitops.git ${GITOPS_DIR}
                    cd ${GITOPS_DIR}

                    sed -i "s|IMAGE_TAG|${BUILD_NUMBER}|g" apps/online-shop/deployment.yaml

                    git config user.email "jenkins@local"
                    git config user.name "jenkins"

                    git add .
                    git commit -m "Update image to ${BUILD_NUMBER}"
                    git push origin main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Secure deployment completed successfully!"
        }
        failure {
            echo "Pipeline failed due to security or quality issues"
        }
    }
}
       