#!/bin/bash
set -e

if [ -S /var/run/docker.sock ]; then

    DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)

    echo "Docker socket GID: ${DOCKER_GID}"

    if ! getent group "${DOCKER_GID}" > /dev/null 2>&1; then
        groupadd -g "${DOCKER_GID}" dockerhost
    fi

    DOCKER_GROUP=$(getent group "${DOCKER_GID}" | cut -d: -f1)

    echo "Docker group: ${DOCKER_GROUP}"

    usermod -aG "${DOCKER_GROUP}" jenkins
fi


exec /usr/bin/tini -- /usr/local/bin/jenkins.sh