# AWS LocalStack

- [AWS LocalStack](#aws-localstack)
  - [Install localstack](#install-localstack)
    - [Community Edition](#community-edition)
  - [AWSLocal CLI](#awslocal-cli)
  - [AWS LocalStack Credentials](#aws-localstack-credentials)
  - [Use localstack](#use-localstack)


## Install localstack 
### Community Edition
```bash
./lstack-docker.sh
```

## AWSLocal CLI
In absence of the `awslocal` wrapper, you can use the aws CLI directly, by configuring an endpoint URL or a custom profile like localstack. You can then swap `awslocal` with `aws --endpoint-url=http://localhost:4566` or `aws --profile=localstack`.

- `awslocal` gets installed by [lstack-docker.sh](./lstack-docker.sh) using `pip` with `--user` flag.

Check [awslocal](./docs/awslocal-cli.md) for usages and examples.

## AWS LocalStack Credentials
By default localstack uses AWS `root` account to authenticate to AWS APIs. Better you create a user and generate secrets, and authenticate to localstack using the user.

Check `Credentials` section in [awslocal-cli](./docs/awslocal-cli.md) to create a new user.

Export the AWS Secrets in OS env to authenticate as new user. Check below shell script example:
```bash
#!/bin/bash
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_DEFAULT_REGION
unset AWS_ENDPOINT_URL

export AWS_ENDPOINT_URL=http://192.168.10.64:4566
function aws_secret(){
    export AWS_ACCESS_KEY_ID=LKIAQAAAAAAAER5BSVAP
    export AWS_SECRET_ACCESS_KEY=vVUGLH6Bge4FNkv4gq0WMHn5ztuQuYQTCb8HgyUW
    export AWS_DEFAULT_REGION="us-east-1"
}
aws_secret
```

## Use localstack
- [Lambda](https://docs.localstack.cloud/user-guide/aws/lambda/)