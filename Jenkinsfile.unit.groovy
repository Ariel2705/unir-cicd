pipeline {
    agent any
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
                sh 'cd /mnt/c || exit 1

                if ls jenkins-results/results/*.xml 1> /dev/null 2>&1; then
                    ts=$(date +%Y%m%d-%H%M%S)
                    mkdir -p jenkins-backup-results/$ts
                    mv jenkins-results/results/*.xml jenkins-backup-results/$ts/
                fi'
            }
        }
        stage('Unit tests') {
            steps {
                sh 'make test-unit'
            }
        }
        stage('API tests') {
            steps {
                sh 'make test-api'
            }
        }
        stage('E2E tests') {
            steps {
                sh 'make test-e2e'
                archiveArtifacts artifacts: 'results/*'
            }
        }
    }
    post {
        always {
            junit 'results/*'
            cleanWs()
        }
    }
}