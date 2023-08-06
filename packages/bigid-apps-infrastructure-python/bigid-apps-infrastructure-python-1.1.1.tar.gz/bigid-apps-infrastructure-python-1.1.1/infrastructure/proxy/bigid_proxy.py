import requests
import ast
import json

from infrastructure.dto.ExecutionContext import ExecutionContext


def fetch_headers(bigid_token):
    return {
        'Content-type': 'application/json; charset=UTF-8',
        'Authorization': bigid_token
    }


def get_request(execution_context: ExecutionContext, endpoint):
    headers = fetch_headers(execution_context.bigid_token)
    return requests.get(execution_context.bigid_base_url + endpoint, headers=headers, verify=False)


def post_request(execution_context: ExecutionContext, endpoint, payload):
    headers = fetch_headers(execution_context.bigid_token)
    return requests.post(execution_context.bigid_base_url + endpoint, headers=headers, verify=False,
                         data=payload)


def put_request(execution_context: ExecutionContext, endpoint, payload):
    headers = fetch_headers(execution_context.bigid_token)
    return requests.put(execution_context.bigid_base_url + endpoint, headers=headers, verify=False,
                        data=payload)


def delete_request(execution_context: ExecutionContext, endpoint, payload):
    headers = fetch_headers(execution_context.bigid_token)
    return requests.delete(execution_context.bigid_base_url + endpoint, headers=headers, verify=False,
                           data=payload)


def send_attachment(execution_context: ExecutionContext, attachment):
    url = execution_context.update_result_callback + "/attachment"

    headers = {
        'authorization': execution_context.bigid_token
    }

    return requests.post(url, headers=headers, data={}, files=[('file', attachment)], verify=False)


def get_app_storage(execution_context: ExecutionContext):
    headers = fetch_headers(execution_context.bigid_token)
    store_in_bigid_url = execution_context.bigid_base_url + "tpa/" + execution_context.tpa_id + "/storage"
    return requests.get(store_in_bigid_url, headers=headers, verify=False)


def get_value_from_app_storage(execution_context: ExecutionContext, key):
    headers = fetch_headers(execution_context.bigid_token)
    store_in_bigid_url = execution_context.bigid_base_url + "tpa/" + execution_context.tpa_id + "/storage"
    value = requests.get(store_in_bigid_url + "/key/" + key, headers=headers, verify=False)
    value_as_dict = ast.literal_eval(value.text)
    if type(value_as_dict) is dict:
        return value_as_dict['value']


def save_in_bigid_storage(execution_context: ExecutionContext, key, value):
    headers = fetch_headers(execution_context.bigid_token)
    store_in_bigid_url = execution_context.bigid_base_url + "tpa/" + execution_context.tpa_id + "/storage"
    keys_values = {'keysValues': [{'key': key, 'value': value}]}
    return requests.put(store_in_bigid_url, headers=headers, verify=False, data=json.dumps(keys_values))
