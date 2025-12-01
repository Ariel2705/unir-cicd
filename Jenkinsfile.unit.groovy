pipeline {
    agent any
    parameters {
        string(name: 'EMAIL_RECIPIENTS', defaultValue: 'hectorarielperez758@gmail.com', description: 'Email recipients for failure notification')
        booleanParam(name: 'SEND_MAIL', defaultValue: false, description: 'If true, actually send the mail; otherwise just echo the content')
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
            script {
                echo '----- Mail preview (failure) -----'
                echo "To: ${env.NOTIFY_RECIPIENTS}"
                echo "Subject: Jenkins: Job '${env.JOB_NAME}' #${env.BUILD_NUMBER} failed"
                echo "Body: The pipeline job '${env.JOB_NAME}' (build #${env.BUILD_NUMBER}) has finished with status: FAILURE. Check ${env.BUILD_URL} for details."
                if (params.SEND_MAIL) {
                    // Uncomment the mail step if you want to send for real. Requires Mailer or Email Extension plugin & SMTP configured in Jenkins
                    mail to: env.NOTIFY_RECIPIENTS,
                         subject: "Jenkins: Job '${env.JOB_NAME}' #${env.BUILD_NUMBER} failed",
                         body: "The pipeline job '${env.JOB_NAME}' (build #${env.BUILD_NUMBER}) has finished with status: FAILURE. Check ${env.BUILD_URL} for details."
                } else {
                    echo "SEND_MAIL is false -> no email sent (only preview logged above)"
                }
            }
        }
    }
}