# AWS LocalStack

- [AWS LocalStack](#aws-localstack)
  - [awslocal CLI](#awslocal-cli)
  - [Install localstack](#install-localstack)
    - [Community Edition](#community-edition)
  - [Use localstack](#use-localstack)

## awslocal CLI
- In absence of the `awslocal` wrapper, you can use the aws CLI directly, by configuring an endpoint URL or a custom profile like localstack. You can then swap `awslocal` with `aws --endpoint-url=http://localhost:4566` or `aws --profile=localstack`.

- `awslocal` gets installed by [lstack-docker.sh](./lstack-docker.sh) using `pip` with `--user` flag.

## Install localstack 
### Community Edition
```bash
./lstack-docker.sh
```

## Use localstack
- [Lambda](https://docs.localstack.cloud/user-guide/aws/lambda/)