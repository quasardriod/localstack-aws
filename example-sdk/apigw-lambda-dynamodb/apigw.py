import boto3
import logging
import zipfile
import os

from common import load_config, AWS_AUTH

logger = logging.getLogger(__name__)

# To send msg to a log file
# logging.basicConfig(filename='aws.log', encoding='utf-8', level=logging.INFO)

# To send msg to stdout
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

class APIGatewayManager(AWS_AUTH):
    def __init__(self, CONFIG):
        # Initialize parent class to load aws secrets
        super().__init__()
        self.CREATE_API_GW = True
        self.client = boto3.client(
            'apigateway',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        )
        self.api_gateway_config = CONFIG['api_gateway']
        self.api_id = None
        # '/' path resource id
        self.root_id = None
        self.stage = None

    def get_rest_api(self):
        apis_list = self.client.get_rest_apis()
        return apis_list

    def create_rest_api(self):
        result = self.client.create_rest_api(name=self.api_gateway_config['name'])
        self.api_id = result["id"]
        logger.info(f"Created REST API {self.api_gateway_config['name']} with ID {self.api_id}")


    def get_root_resource_id(self):
        resources = self.client.get_resources(restApiId=self.api_id)
        self.root_id = [resource['id'] for resource in resources['items'] if resource['path'] == '/'][0]
        logger.info(f"API GW ID: {self.api_id} Root resource's ID: {self.root_id} of path '/'")

    def create_resource_and_method(self):
        for resource in self.api_gateway_config['resources']:
            # Create a new resource under the root resource
            resource_response = self.client.create_resource(
                restApiId=self.api_id,
                parentId=self.root_id,
                pathPart=resource['pathPart']
            )
            resource_id = resource_response['id']
            logger.info(f"API GW ID: {self.api_id} -> Created resource '{resource['pathPart']}' with ID: {resource_id}")

            # Create a new method on the resource
            self.client.put_method(
                restApiId=self.api_id,
                resourceId=resource_id,
                httpMethod=resource['httpMethod'],
                authorizationType=resource['authorizationType'],
                requestParameters=resource['requestParameters']
            )
            logger.info(f"API GW ID: {self.api_id} -> Created {resource['httpMethod']} method for '{resource['pathPart']}' resource")

    def setup_api_gateway(self):

        apis_list = self.get_rest_api()
        # print(apis_list)
        for _api in apis_list['items']:
            if _api['name'] == self.api_gateway_config['name']:
                self.CREATE_API_GW = False
                logger.warning(f"API Gateway '{self.api_gateway_config['name']}' already exists. ID: {_api['id']}")
                break
        
        if self.CREATE_API_GW:
            self.create_rest_api()
            self.get_root_resource_id()
            self.create_resource_and_method()

class LambdaManager(AWS_AUTH):
    def __init__(self, region_name='us-east-1'):
        super().__init__()
        # Initialize a Boto3 client for Lambda
        self.lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
        )

    def create_zip_file(self, function_name):
        """
        Create a ZIP file of the Lambda function.
        """
        zip_file = f'{function_name}.zip'
        with zipfile.ZipFile(zip_file, 'w') as z:
            z.write(f'{function_name}.py')
        return zip_file

    def create_lambda_function(self, function_name, role_arn, runtime='python3.8', timeout=10, memory_size=128, description='A Lambda function created with Python'):
        """
        Create a Lambda function using the provided parameters.
        """
        # Zip the Lambda function code
        zip_file = self.create_zip_file(function_name)
        
        # Create the Lambda function
        with open(zip_file, 'rb') as zip_data:
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=role_arn,
                Handler=f'{function_name}.lambda_handler',
                Code={
                    'ZipFile': zip_data.read(),
                },
                Description=description,
                Timeout=timeout,  # Set the timeout (in seconds)
                MemorySize=memory_size,  # Set memory size (in MB)
                Publish=True
            )
        
        # Clean up the zip file
        os.remove(zip_file)
        
        print(f"Created Lambda function with ARN: {response['FunctionArn']}")
        return response

    def invoke_lambda_function(self, function_name, payload):
        """
        Invoke the Lambda function with a given payload.
        """
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        response_payload = response['Payload'].read().decode('utf-8')
        print(f"Response from Lambda function: {response_payload}")
        return response_payload


# Example usage
if __name__ == "__main__":
    # Initialize the LambdaManager
    lambda_manager = LambdaManager(region_name='us-east-1')
    
    # Set the function name and role ARN
    function_name = 'MyLambdaFunction'
    role_arn = '<your-iam-role-arn>'
    
    # Create the Lambda function
    lambda_manager.create_lambda_function(
        function_name=function_name,
        role_arn=role_arn,
        description='A simple example Lambda function created with Python',
        timeout=10,
        memory_size=128
    )
    
    # Optional: Invoke the Lambda function with a sample payload
    sample_payload = {"key": "value"}
    lambda_manager.invoke_lambda_function(function_name=function_name, payload=sample_payload)


if __name__ == "__main__":
    CONFIG = load_config()
    manager = APIGatewayManager(CONFIG)
    manager.setup_api_gateway()
