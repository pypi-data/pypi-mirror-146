import os
import boto3
import logging
from quickbelog import Log

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

for log_name in ['boto', 'boto3', 'botocore', 's3transfer', 'urllib3']:
    logging.getLogger(log_name).setLevel(logging.WARNING)

ssm_client = boto3.client('ssm')


def get_env_as_list(key: str, default: list = None) -> list:
    values = os.getenv(key)
    if values is None:
        values = default
    elif isinstance(values, str):
        values = [val.strip() for val in values.split(',')]
    return values


def get_parameters(path: str = '/', update_environ: bool = True, dump_parameters: bool = True) -> dict:
    if not path.startswith('/'):
        path = f'/{path}'
    try:
        paginator = ssm_client.get_paginator('describe_parameters')
        pager = paginator.paginate(
            ParameterFilters=[
                dict(Key="Path", Option="Recursive", Values=[path])
            ]
        )
        parameters_data = {}
        for page in pager:
            parameters = [p_data['Name'] for p_data in page['Parameters'] if 'Name' in p_data]
            parameters_data.update(_get_parameters_value(parameters=parameters, path=path))
        Log.info(f'Retrieved {len(parameters_data)} variables from Parameter Store from {path}.')
        if dump_parameters:
            dump(parameters_data)
        if update_environ:
            if parameters_data is not None and isinstance(parameters_data, dict):
                os.environ.update(parameters_data)
        return parameters_data
    except Exception:
        Log.exception(f'Can not access AWS parameter store, path: {path}.')


def _get_parameters_value(parameters: list, path: str) -> dict:
    result = {}
    parameters_data = ssm_client.get_parameters(Names=parameters, WithDecryption=True)
    for p in parameters_data['Parameters']:
        p_path = str(p['Name'])
        p_name = p_path.replace(f'{path}/', '').replace('/', '_').upper()
        result[p_name] = p.get('Value', '')
    return result


def dump(d: dict):
    for k, v in sorted(d.items()):
        if _is_secret(k):
            v = '*' * len(v)
        Log.debug(f'{k}: {v}')


AWS_VAULT_SECRET_SUFFIXES = get_env_as_list(
    key='AWS_VAULT_SECRET_SUFFIXES',
    default=['PWD', 'PASSWORD', 'TOKEN', 'SECRET', '_KEY', '_KEYS']
)
AWS_VAULT_SECRET_WORDS = get_env_as_list(
    key='AWS_VAULT_SECRET_WORDS',
    default=['PASSWORD', 'ACCESS_KEY', 'SECRET_KEY', '_PWD_']
)


def _is_secret(s: str) -> bool:
    s_up = s.upper().strip()
    for word in AWS_VAULT_SECRET_WORDS:
        if word in s_up:
            return True
    for word in AWS_VAULT_SECRET_SUFFIXES:
        if s_up.endswith(word):
            return True
    return False
