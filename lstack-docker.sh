#!/bin/bash

image="localstack/localstack:latest"
container=localstack

pro_image="localstack/localstack-pro:latest"
pro_container=localstack-pro

container_map_ip="0.0.0.0" # Also can use 127.0.0.1

default_interface=$(ls -l /sys/class/net/|awk '{print $9}'|egrep ^e)

if ! ip address show dev $default_interface >/dev/null 2>&1;then
    printf "\nERROR: Failed to read ip address from $default_interface\n"
    exit 1
else
    machine_ip=$(ip address show dev $default_interface|egrep "^\s+inet\s"|awk '{print $2}'|cut -d'/' -f1|xargs)
fi

function additional_tools(){
    if ! which git >/dev/null 2>&1;then
        printf "\nINFO: Installing git...\n"
        dnf install -y -q \
        git jq zip
    fi
}

function install_awscli(){
    if ! which pip3 >/dev/null 2>&1;then
        printf "\nINFO: Installing pip...\n"
        dnf install python3-pip -y -q
    fi
    if ! which $HOME/.local/bin/awslocal >/dev/null 2>&1;then
        printf "\nINFO: Installing aws and awslocal CLI...\n"
        pip3 install awscli awscli-local --user
    fi  
}

function install_docker(){
    if ! which docker >/dev/null 2>&1;then
        printf "\nINFO: Installing docker...\n"
        dnf install -y -q yum-utils
        
        # Configure docker repo
        yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        
        # Install docker packages
        dnf install -y -q \
        docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

        # Start docker service
        systemctl start docker
        systemctl enable docker
    fi
}

function stack_image(){
    printf "\nINFO: Pull localstack image: $1\n"
    docker pull $1
}

function install_localstack_non_pro(){
    printf "\nINFO: Running NON-Pro localstack in docker container...\n"
    docker run \
    --rm -it -d \
    --name $container \
    -p $container_map_ip:4566:4566 \
    -p $container_map_ip:4510-4559:4510-4559 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    $image
}

function install_localstack_pro(){
    printf "\nINFO: Running Pro localstack in docker container...\n"
    docker run \
    --rm -it -d \
    --name $pro_container \
    -p $container_map_ip:4566:4566 \
    -p $container_map_ip:4510-4559:4510-4559 \
    -e LOCALSTACK_AUTH_TOKEN=${LOCALSTACK_AUTH_TOKEN:- } \
    -v /var/run/docker.sock:/var/run/docker.sock \
    $pro_image
}

function main(){
    install_docker
    additional_tools

    [ -f .lstackenv ] && source .lstackenv
    # Check for LOCALSTACK_AUTH_TOKEN
    if [ -z $LOCALSTACK_AUTH_TOKEN ];then
        printf "\nINFO: LOCALSTACK_AUTH_TOKEN not found, running localstack with non-pro image\n"
        stack_image $image
        install_localstack_non_pro
    else
        stack_image $pro_image
        install_localstack_pro
    fi
    
    install_awscli
    
    [ -z $machine_ip ] && printf "\nERROR: Failed to get machine IP\n" && exit 1
    printf "\nINFO: Running below command to check license information.\n -> curl -s http://$machine_ip:4566/_localstack/info | jq\n"
    sleep 30
    curl -s http://$machine_ip:4566/_localstack/info | jq

    printf "\nINFO: List configuration using awslocal...\n $(awslocal configure list)\n"
}

main
