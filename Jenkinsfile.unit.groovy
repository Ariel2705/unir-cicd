pipeline {
    agent any
    environment {
        NOTIFY_RECIPIENTS = 'hectorarielperez758@gmail.com'
    }
    stages {
        stage('Source') {
            steps {
                git 'https://github.com/Ariel2705/unir-cicd.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building stage!'
                sh 'make build'
            }
        }
        stage('Backup') {
            steps {
                sh '''
                exit 1
                cd /results || exit 1

                if [ "$(ls .)" ]; then
                    ts=$(date +%Y%m%d-%H%M%S)
                    mkdir -p backup-results/$ts
                    mv ./results/* backup-results/$ts/ 
                    rm -rf ./results                    
                fi
                '''
            }
        }
        stage('Unit tests') {
            steps {
                sh 'make test-unit'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        stage('API tests') {
            steps {
                sh 'make test-api'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        stage('E2E tests') {
            steps {
                sh 'make test-e2e'
                archiveArtifacts artifacts: 'results/*.json'
            }
        }
    }
    post {
        always {
            junit 'results/*.xml'
            cleanWs()
        }
        failure {
            mail to: env.NOTIFY_RECIPIENTS,
                 subject: "Jenkins: Job '${env.JOB_NAME}' #${env.BUILD_NUMBER} failed",
                 body: "The pipeline job '${env.JOB_NAME}' (build #${env.BUILD_NUMBER}) has finished with status: FAILURE. \n\nCheck the build console output at ${env.BUILD_URL} for details."
        }
    }
}