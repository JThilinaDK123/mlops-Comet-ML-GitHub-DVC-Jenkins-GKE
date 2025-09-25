pipeline {
    agent any

    environment {
        VENV_DIR   = 'venv'
        GCP_PROJECT = "mlops-thilina"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
        IMAGE_NAME  = "gcr.io/mlops-thilina/mlops-app-project-06:latest"
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
                            credentialsId: 'GitHub-token', 
                            url: 'https://github.com/JThilinaDK123/mlops-Comet-ML-GitHub-DVC-Jenkins-GKE.git'
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
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }

        stage('DVC Pull') {
            steps {
                withCredentials([file(credentialsId: 'gcp-json-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'DVC Pull............'
                        sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
                        . ${VENV_DIR}/bin/activate
                        dvc pull --force
                        '''
                    }
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-json-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker buildx create --use || true
                        docker buildx inspect --bootstrap

                        # Build and push for linux/amd64
                        docker buildx build --platform linux/amd64 -t ${IMAGE_NAME} . --push

                        '''
                    }
                }
            }
        }

        // stage('Train Model') {
        //     steps {
        //         withCredentials([file(credentialsId: 'gcp-json-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        //             script {
        //                 echo 'Running Training Pipeline............'
        //                 sh '''
        //                 export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
        //                 . ${VENV_DIR}/bin/activate
        //                 python pipeline/training_pipeline.py
        //                 '''
        //             }
        //         }
        //     }
        // }

        stage('Deploy to Google Kubernetes Engine') {
            steps{
                withCredentials([file(credentialsId: 'gcp-json-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Kubernetes Engine.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials mlops-project-06-cluster --zone us-central1
                        kubectl apply -f kubernetes-deployment.yaml
                        
                        '''
                    }
                }
            }
        }
    }
}
