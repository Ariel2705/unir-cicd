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
        /*stage('Backup') {
            steps {
                sh '''
                cd /results || exit 1

                if [ "$(ls -A)" ]; then
                    ts=$(date +%Y%m%d-%H%M%S)
                    mkdir -p jenkins-backup-results/$ts
                    mv ./* jenkins-backup-results/$ts/ 2>/dev/null
                fi
                '''
            }
        }*/
        stage('Unit tests') {
            steps {
                sh 'make test-unit'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        stage('API tests') {
            steps {
                sh 'make test-api'
                archiveArtifacts artifacts: '/results/*.xml'
            }
        }
        /*stage('E2E tests') {
            steps {
                //sh 'make test-e2e'
                archiveArtifacts artifacts: '/results/*.xml'
            }
        }*/
    }
    post {
        always {
            junit '/results/*.xml'
            cleanWs()
        }
    }
}