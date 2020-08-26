from functools import wraps
from importlib import import_module
from cerberus import Validator as get_check
from os.path import dirname, isfile, join, basename
from flask import request, jsonify
from glob import glob
import json

modules = glob(join(dirname(__file__), "*.py"))


def get_handler(schema, name, route):
    struct = {
        'body': 'body' in schema and {'schema': schema['body']} or {},
        'headers': 'headers' in schema and {'schema': schema['headers']} or {},
        'query': 'query' in schema and {'schema': schema['query']} or {},
        'params': 'params' in schema and {'schema': schema['params']} or {}
    }
    check = get_check(struct)
    check({})  # Saves time on the first call

    @wraps(route)
    def handler(**params):
        query, body = request.args.to_dict(), request.get_json()
        body = body if body else request.form.to_dict()
        body = json.loads(body) if type(body) == str else body
        headers, values = {}, request.headers.values()
        for key in request.headers.keys():
            headers[key] = values.__next__()
        incoming = {'body': body, 'headers': headers,
                    'query': query, 'params': params}
        custom = True if 'custom' not in schema else schema['custom'](incoming)
        if custom != True:
            response = jsonify({'message': 'Request Error', 'errors': custom})
            response.status_code = 400
            return response
        if check(incoming) == False:
            response = jsonify(
                {'message': 'Request Error', 'errors': check.errors})
            response.status_code = 400
            return response
        result = route(incoming)
        if type(result) != dict:
            return result

        response = jsonify(result['body'])
        response.status_code = result['status']
        return response
    return handler


def define_routes(app):
    for file in modules:
        if isfile(file) and not file.endswith('__init__.py'):
            key = basename(file)[:-3]
            schema = import_module('api.routes.schemas.' + key).schema
            for name in schema.keys():
                if 'paths' not in schema[name]:
                    print('No paths provided for endpoint',
                          name, 'of schema', key)
                    continue
                paths = schema[name]['paths']
                paths_type = type(paths)
                if paths_type not in [str, list]:
                    print('Type for path must be str or list, endpoint:',
                          name, ', schema:', key)
                    continue
                if paths_type == str:
                    paths = [paths]
                route = __import__('api.routes.' + key, fromlist=[name])
                route = getattr(route, name)
                if (callable(route)):
                    handler = get_handler(schema[name], name, route)
                    for path in paths:
                        methods = schema[name]['methods']
                        app.route(path, methods=methods)(handler)
