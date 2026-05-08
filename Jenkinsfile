pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                credentialsId: 'github-token',
                url: 'https://github.com/SyedNasirUddin/Hotel_Reservations_MLOPS.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t hotel-mlops .'
            }
        }

        stage('Run Docker Container') {
            steps {

                sh 'docker stop hotel-container || true'
                sh 'docker rm hotel-container || true'

                sh '''
                docker run -d \
                --name hotel-container \
                -p 5000:5000 \
                hotel-mlops
                '''
            }
        }
    }
}