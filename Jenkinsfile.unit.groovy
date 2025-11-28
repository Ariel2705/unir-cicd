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
        stage('Unit tests') {
            steps {
                sh 'make test-unit'
                archiveArtifacts artifacts: '/opt/results/*.xml'
            }
        }
    }
    post {
        always {
            junit '/opt/results/*_result.xml'
            cleanWs()
        }
    }
}