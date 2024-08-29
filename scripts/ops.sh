#!/bin/bash

source scripts/constant.sh

[ -z $AWS_ENDPOINT_URL ] && error "\nERROR: AWS_ENDPOINT_URL env var not set\n" 

function get_user(){
    awslocal iam list-users
}


function main(){
    get_user
}

main