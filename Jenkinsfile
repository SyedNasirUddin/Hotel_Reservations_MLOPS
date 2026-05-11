pipeline {

    agent any

    environment {

        VENV_DIR = 'venv'

        GCP_PROJECT = "oval-airship-465513-m2"

        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Cloning Github repo to Jenkins') {

            steps {

                script {

                    echo 'Cloning Github repo to Jenkins............'

                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/SyedNasirUddin/Hotel_Reservations_MLOPS.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up Virtual Environment and Installing Dependencies') {

            steps {

                script {

                    echo 'Setting up Virtual Environment and Installing Dependencies............'

                    sh '''
                    python3 -m venv ${VENV_DIR}

                    . ${VENV_DIR}/bin/activate

                    python3 -m pip install --upgrade pip setuptools wheel

                    python3 -m pip install --default-timeout=100 --no-cache-dir -r requirements.txt
                    '''
                }
            }
        }

        stage('Training ML Model') {

            steps {

                script {

                    echo 'Training ML Model............'

                    sh '''
                    . ${VENV_DIR}/bin/activate


                    export PYTHONPATH=$WORKSPACE


                    python pipeline/training_pipeline.py
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR') {

            steps {

                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {

                    script {

                        echo 'Building and Pushing Docker Image to GCR............'

                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/hotel-reservation-app:latest .

                        docker push gcr.io/${GCP_PROJECT}/hotel-reservation-app:latest
                        '''
                    }
                }
            }
        }
    }

    post {

        success {

            echo 'Pipeline executed successfully!'
        }

        failure {

            echo 'Pipeline failed!'
        }
    }
}