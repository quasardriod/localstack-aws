
- [Set Endpoint](#set-endpoint)
- [Credentials](#credentials)
- [API Gateway](#api-gateway)
  - [API Gateway Resource](#api-gateway-resource)
    - [Create a resource](#create-a-resource)
    - [Method](#method)
    - [Integration](#integration)

## Set Endpoint
***
Source: https://docs.localstack.cloud/user-guide/integrations/aws-cli/
```bash
export AWS_ENDPOINT_URL=http://192.168.10.64:4566
```

## Credentials
***
Refer official doc for more information on [IAM](https://docs.localstack.cloud/user-guide/aws/iam/).

- Get default caller identity
```bash
[root@localstack ~]# awslocal sts get-caller-identity
{
    "UserId": "AKIAIOSFODNN7EXAMPLE",
    "Account": "000000000000",
    "Arn": "arn:aws:iam::000000000000:root"
}
```

- Create User
```json
$ awslocal iam create-user --user-name boso
{
    "User": {
        "Path": "/",
        "UserName": "boso",
        "UserId": "lu0j1t96d3co5fxfs871",
        "Arn": "arn:aws:iam::000000000000:user/boso",
        "CreateDate": "2024-08-28T17:30:07.803000Z"
    }
}
```

- Create Access key
```json
$ awslocal iam create-access-key --user-name boso
{
    "AccessKey": {
        "UserName": "boso",
        "AccessKeyId": "LKIAQAAAAAAAAZHGRYLK",
        "Status": "Active",
        "SecretAccessKey": "iy7bUQ1w6mp01cKDUg30QwGSgY47Dcz2lgi2gn9h",
        "CreateDate": "2024-08-28T17:31:09Z"
    }
}
```

- After exporting `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, `get-caller-identity` would show created user identity.
```bash
export AWS_ACCESS_KEY_ID=LKIAQAAAAAAAAZHGRYLK
export AWS_SECRET_ACCESS_KEY=iy7bUQ1w6mp01cKDUg30QwGSgY47Dcz2lgi2gn9h
$ awslocal sts get-caller-identity
{
    "UserId": "lu0j1t96d3co5fxfs871",
    "Account": "000000000000",
    "Arn": "arn:aws:iam::000000000000:user/boso"
}
```

## API Gateway
***
- Create API Gateway
```bash
$ awslocal apigateway create-rest-api --name 'API Gateway Lambda integration'
{
    "id": "ri1n0p1k3n",
    "name": "API Gateway Lambda integration",
    "createdDate": 1724867066.0,
    "apiKeySource": "HEADER",
    "endpointConfiguration": {
        "types": [
            "EDGE"
        ]
    },
    "disableExecuteApiEndpoint": false,
    "rootResourceId": "y45klm8qze"
}
```
- Other `apigateway` command
```bash
# Get All created api gw
awslocal apigateway get-rest-apis

# Get specific api gw
awslocal apigateway get-rest-api --rest-api-id ri1n0p1k3n

# Delete a specific api gw
awslocal apigateway delete-rest-api --rest-api-id fiu5u88r8h
```

### API Gateway Resource
- Get default resource of new created api gw
    - By default on creating api gw, it will create default resource with path `/`, which we can see in below example.
    - Returned resource ID with path `/` also referred as `parent_id`, which will be used to create further resources.
```bash
$ awslocal apigateway get-resources --rest-api-id ri1n0p1k3n
{
    "items": [
        {
            "id": "y45klm8qze",
            "path": "/"
        }
    ]
}
```

#### Create a resource
Resources are generally endpoints available/published by API to users.

```bash
# In --path-part option provide a string(a path) that you want to expose using api gw. In the output we can see value provided in --path-part used for a subpath of the urls those will be published by api.
$ awslocal apigateway create-resource \
  --rest-api-id ri1n0p1k3n \
  --parent-id y45klm8qze \
  --path-part "hellolambda"

{
    "id": "7ugv75xidw",
    "parentId": "y45klm8qze",
    "pathPart": "hellolambda",
    "path": "/hellolambda"
}
```

- Other command options of API GW Resources
```bash
# List all resources
$ awslocal apigateway get-resources --rest-api-id ri1n0p1k3n
{
    "items": [
        {
            "id": "y45klm8qze",
            "path": "/"
        },
        {
            "id": "7ugv75xidw",
            "parentId": "y45klm8qze",
            "pathPart": "hellolambda",
            "path": "/hellolambda"
        }
    ]
}
```

#### Method
Set CRUD methods like GET, POST, PUT, PATCH, DELETE on created resources.

```bash
$ awslocal apigateway put-method \
  --rest-api-id ri1n0p1k3n \
  --resource-id 7ugv75xidw \
  --http-method GET \
  --request-parameters "method.request.path.hellolambda=true" \
  --authorization-type "NONE"

{
    "httpMethod": "GET",
    "authorizationType": "NONE",
    "apiKeyRequired": false,
    "requestParameters": {
        "method.request.path.hellolambda": true
    }
}
```

#### Integration
Integration of other services to API GW.