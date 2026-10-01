pipeline {

    // Выполняем Pipeline на доступном Jenkins-агенте.
    agent any

    // Переменные, доступные во всех этапах.
    environment {
        // Имя Docker-образа приложения.
        IMAGE_NAME = "calculate-api"
    }

    stages {

        // Jenkins уже автоматически скачивает код из GitHub,
        // но здесь выводим информацию о текущем commit.
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

        // Создаём изолированное Python-окружение и устанавливаем
        // зависимости, нужные для тестирования.
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

        // Запускаем тесты. Если pytest завершится с ошибкой,
        // следующие этапы, включая Docker build и deploy, не запустятся.
        stage('Test') {
            steps {
                sh '''
                    echo "===== Running tests ====="

                    .venv-ci/bin/python -m pytest
                '''
            }
        }

        // Формируем новую версию на основе номера сборки Jenkins.
        //
        // Build #1 -> 1.0.1
        // Build #2 -> 1.0.2
        // Build #3 -> 1.0.3
        stage('Generate version') {
            steps {
                script {
                    env.APP_VERSION = "1.0.${env.BUILD_NUMBER}"
                }

                sh '''
                    echo "===== Application version ====="
                    echo "${APP_VERSION}"

                    # VERSION попадёт внутрь Docker-образа,
                    # потому что Dockerfile содержит COPY VERSION ./VERSION.
                    echo "${APP_VERSION}" > VERSION
                '''
            }
        }

        // Собираем новую версию приложения и создаём тег latest.
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

        // Удаляем старый контейнер и запускаем новый.
        stage('Deploy') {
            steps {
                sh '''
                    echo "===== Deploying Calculator API ====="

                    # Если контейнера calculator ещё нет,
                    # команда завершится ошибкой, но || true не даст
                    # Jenkins считать это ошибкой Pipeline.
                    docker rm -f calculator || true

                    # Запускаем новую версию API.
                    docker run -d \
                        --name calculator \
                        -p 8000:8000 \
                        ${IMAGE_NAME}:${APP_VERSION}

                    echo "Deployed version: ${APP_VERSION}"
                '''
            }
        }

        // Проверяем, что новый контейнер реально отвечает по /health.
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