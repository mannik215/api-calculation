pipeline {
    // Где Jenkins может выполнять Pipeline.
    // any = на любом доступном агенте.
    agent any

    // Глобальные переменные окружения.
    environment {
        // Имя собираемого Docker-образа.
        IMAGE_NAME = "calculate-api"
    }

    // Здесь находятся этапы CI.
    stages {

        stage('Checkout') {
            steps {
                // Jenkins при использовании "Pipeline script from SCM"
                // уже скачивает репозиторий автоматически.
                //
                // Здесь просто проверяем, какой код был получен.
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
                // Создаём отдельное виртуальное окружение
                // именно для текущей CI-сборки.
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
                // Запускаем pytest.
                //
                // Если хотя бы один тест завершится ошибкой,
                // pytest вернёт ненулевой exit code.
                //
                // Jenkins автоматически остановит Pipeline.
                sh '''
                    echo "===== Running tests ====="

                    .venv-ci/bin/python -m pytest
                '''
            }
        }

        stage('Build Docker') {
            steps {
                sh '''
                    echo "===== Reading application version ====="

                    VERSION=$(cat VERSION)

                    echo "Building ${IMAGE_NAME}:${VERSION}"

                    # Docker читает Dockerfile приложения
                    # из корня репозитория.
                    docker build \
                        -t ${IMAGE_NAME}:${VERSION} \
                        .

                    # Тот же образ получает дополнительный тег latest.
                    docker tag \
                        ${IMAGE_NAME}:${VERSION} \
                        ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    // Действия после завершения stages.
    post {
        success {
            echo 'SUCCESS: tests passed and Docker image was built.'
        }

        failure {
            echo 'FAILURE: check Console Output.'
        }

        always {
            echo 'Calculator CI pipeline finished.'
        }
    }
}