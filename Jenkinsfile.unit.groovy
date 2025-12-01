pipeline {
    agent any
    parameters {
        string(name: 'EMAIL_RECIPIENTS', defaultValue: 'hectorarielperez758@gmail.com')
        booleanParam(name: 'SEND_MAIL', defaultValue: false)
    }
    environment {
        NOTIFY_RECIPIENTS = "${params.EMAIL_RECIPIENTS}"
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
            script {
                echo '----- Mail (failure) -----'
                echo "To: ${env.NOTIFY_RECIPIENTS}"
                echo "Subject: Jenkins: Falló el Job '${env.JOB_NAME}' #${env.BUILD_NUMBER}"
                echo "Body: El pipeline job '${env.JOB_NAME}' (build #${env.BUILD_NUMBER}) ha terminado con estado: FAILURE. Revisar ${env.BUILD_URL} para más detalles."
                if (params.SEND_MAIL) {
                    mail to: env.NOTIFY_RECIPIENTS,
                         subject: "Jenkins: Falló el Job '${env.JOB_NAME}' #${env.BUILD_NUMBER}",
                         body: "El pipeline job '${env.JOB_NAME}' (build #${env.BUILD_NUMBER}) ha terminado con estado: FAILURE. Revisar ${env.BUILD_URL} para más detalles."
                } else {
                    echo "SEND_MAIL es false por lo que solamente se puede ver el preview"
                }
            }
        }
    }
}