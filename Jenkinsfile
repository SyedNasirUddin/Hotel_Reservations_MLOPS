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

        stage('Building and Pushing Docker Image to Artifact Registry') {

            steps {

                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {

                    script {

                        echo 'Building and Pushing Docker Image to Artifact Registry............'

                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        cat ${GOOGLE_APPLICATION_CREDENTIALS} | docker login -u _json_key --password-stdin https://us-central1-docker.pkg.dev

                        docker build -t us-central1-docker.pkg.dev/${GCP_PROJECT}/hotel-repo/hotel-reservation-app:latest .

                        docker push us-central1-docker.pkg.dev/${GCP_PROJECT}/hotel-repo/hotel-reservation-app:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run') {

            steps {

                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {

                    script {

                        echo 'Deploying application to Google Cloud Run............'

                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy hotel-reservation-service \
                        --image=us-central1-docker.pkg.dev/${GCP_PROJECT}/hotel-repo/hotel-reservation-app:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow=unauthenticated \
                        --port=8080 \
                        --quiet
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

