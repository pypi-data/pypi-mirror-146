import os

def get_environment():
    env = os.getenv('APP_ENVIRONMENT')
    if env == None:
        raise Exception("Environment is not set. Set Production or Development by calling 'python Environment.py <env_name>'")
    return env

def set_environment(envirment_name):
    os.environ['APP_ENVIRONMENT'] = envirment_name
    print('Environment is set to -> ' + os.getenv('APP_ENVIRONMENT'))

