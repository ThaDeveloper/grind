#!/bin/bash
APP_VERSION=$(git rev-parse --short HEAD)

install_aws_cli(){
    echo "====> Installing aws cli"
    sudo apt-get update && sudo apt-get install awscli
}

reg_login() {
	echo "Logging into docker image registry..."
	eval $(aws ecr get-login --no-include-email | sed 's|https://||')
}

tag_and_publish() {
    make tag ${APP_VERSION}
    make push
}

docker_logout() {
    docker logout ${DOCKER_REGISTRY}
}
	
main(){
    install_aws_cli
    reg_login
    tag_and_publish
    docker_logout
}
main
