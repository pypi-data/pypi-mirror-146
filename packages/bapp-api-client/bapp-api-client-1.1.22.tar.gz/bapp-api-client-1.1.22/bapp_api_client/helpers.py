from bapp_api_client.api_client import ApiClient
from bapp_api_client.configuration import Configuration


def get_bapp_user_client(token: str, debug: bool = False):
    configuration = Configuration()
    configuration.api_key_prefix['Authorization'] = 'Token'
    configuration.api_key['Authorization'] = token
    configuration.debug = debug
    client = ApiClient(configuration)
    return client

def get_bapp_company_client(token: str, company_id:int, debug: bool = False):
    configuration = Configuration()
    configuration.api_key_prefix['Authorization'] = 'Token'
    configuration.api_key['Authorization'] = token
    configuration.debug = debug
    client = ApiClient(configuration, header_name='x-company-id', header_value=str(company_id))
    return client
