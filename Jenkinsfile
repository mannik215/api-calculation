pipeline {


    agent any


    environment {

        IMAGE_NAME = "calculate-api"
    }

    stages {


        stage('Checkout') {
            steps {
                sh '''
                    echo "===== Git information ====="
                    git log -1 --oneline

                    echo "===== Project files ====="
                    ls -la
                '''
            }
        }


        stage('Install dependencies') {
            steps {
                sh '''
                    echo "===== Creating Python venv ====="

                    python3 -m venv .venv-ci

                    echo "===== Installing dependencies ====="

                    .venv-ci/bin/python -m pip install --upgrade pip
                    .venv-ci/bin/python -m pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "===== Running tests ====="

                    .venv-ci/bin/python -m pytest
                '''
            }
        }
        stage('Security - Semgrep SAST') {
            steps {
                sh '''
                    echo "===== Semgrep SAST ====="

                    docker run --rm \
                        -v "$WORKSPACE:/src" \
                        semgrep/semgrep \
                        semgrep scan \
                        --config auto \
                        /src/app
                '''
            }
        }
        // stage('Security - Dependency Audit') {
        //     steps {
        //         sh '''
        //             echo "===== Python dependency audit ====="

        //             .venv-ci/bin/python -m pip install pip-audit

        //             .venv-ci/bin/python -m pip_audit \
        //                 -r requirements.txt
        //         '''
        //     }
        // }

        stage('Generate version') {
            steps {
                script {
                    env.APP_VERSION = "1.0.${env.BUILD_NUMBER}"
                }

                sh '''
                    echo "===== Application version ====="
                    echo "${APP_VERSION}"

                    echo "${APP_VERSION}" > VERSION
                '''
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                    echo "===== Building Docker image ====="
                    echo "Image: ${IMAGE_NAME}:${APP_VERSION}"

                    docker build \
                        -t ${IMAGE_NAME}:${APP_VERSION} \
                        .

                    docker tag \
                        ${IMAGE_NAME}:${APP_VERSION} \
                        ${IMAGE_NAME}:latest
                '''
            }
        }
        // stage('Security - Trivy Image Scan') {
        //     steps {
        //         sh '''
        //             docker run --rm \
        //                 -v /var/run/docker.sock:/var/run/docker.sock \
        //                 -v "$WORKSPACE:/reports" \
        //                 aquasec/trivy:latest \
        //                 image \
        //                 --severity HIGH,CRITICAL \
        //                 --format json \
        //                 --output /reports/trivy-report.json \
        //                 ${IMAGE_NAME}:${APP_VERSION}
        //         '''

        //         archiveArtifacts artifacts: 'trivy-report.json'
        //     }
        // }
        // stage('Security - Secrets Scan') {
        //     steps {
        //         sh '''
        //             docker run --rm \
        //                 -v "$WORKSPACE:/src" \
        //                 aquasec/trivy:latest \
        //                 fs \
        //                 --scanners secret \
        //                 /src
        //         '''
        //     }
        // }

        stage('Deploy') {
            steps {
                sh '''
                    echo "===== Deploying Calculator API ====="


                    docker rm -f calculator || true

                    docker run -d \
                        --name calculator \
                        -p 8000:8000 \
                        ${IMAGE_NAME}:${APP_VERSION}

                    echo "Deployed version: ${APP_VERSION}"
                '''
            }
        }

        stage('Verify deployment') {
            steps {
                sh '''
                    echo "===== Checking deployed application ====="

                    # Даём Uvicorn несколько секунд на запуск.
                    sleep 5

                    python3 - <<'PY'
import json
import urllib.request

response = urllib.request.urlopen(
    "http://host.docker.internal:8000/health",
    timeout=10,
)

data = json.load(response)

print("Health response:", data)

if data["status"] != "ok":
    raise SystemExit("Health check failed")

print("Deployment verification passed.")
PY
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: tests passed, image built, application deployed.'
        }

        failure {
            echo 'FAILURE: check Jenkins Console Output.'
        }

        always {
            echo 'Calculator CI/CD pipeline finished.'
        }
    }
}