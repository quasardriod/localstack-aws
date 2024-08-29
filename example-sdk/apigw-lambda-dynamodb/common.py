import yaml
import os

CONFIG_FILE='config.yaml'

# Function to load the YAML configuration file
def load_config():
    app_dir = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists(f'{app_dir}/{CONFIG_FILE}'):
        print(f"ERROR: Could not find {CONFIG_FILE} in {app_dir}")
        return False

    with open(f'{app_dir}/{CONFIG_FILE}', 'r') as file:
        try:
            CONFIG=yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print (f"ERROR: Failed to parse {CONFIG_FILE}")
            return False
    return CONFIG

class AWS_AUTH:
    def __init__(self):
        # Read AWS Secrets from OS Env
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.getenv('AWS_DEFAULT_REGION')
        self.endpoint_url = os.getenv('AWS_ENDPOINT_URL')