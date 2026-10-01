pipeline{
    agent any
    environment{
        IMAGE_NAME="calculate_api"
    }
    stages {
        stage ('Upadate versions') {
            steps{
                sh 'python3 scripts/update_version.py'
            }
        }
        stage('Test'){
            steps{
                sh 'python3 -m pip install -r requirements-dev.txt && pytest'
            }
        }
        stage('Build Docker'){
            steps{
                sh '''
                VERSION=$(cat VERSION)
                echo "Building $IMAGE_NAME:$VERSION"
                docker build -t $IMAGE_NAME:$VERSION .
                docker tag $IMAGE_NAME:$VERSION $IMAGE_NAME:latest
                '''
            }
        }
    }
    post{
        always {
            echo 'Pipeline finished for calculator API'

        }
        failure {
            echo 'FAILURE: Tests or Docker build failed.'

        }
        success{
            echo 'SUCCESS: Test done, new versions built and tagged'
        }
    }

}