from functools import wraps
from importlib import import_module
from cerberus import Validator as get_check
from os.path import dirname, basename, isfile, join
from flask import request, jsonify
from json import dumps
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))


def get_handler(schema, name, route):
    struct = {
        'body': 'body' in schema and schema['body'] or {},
        'headers': 'headers' in schema and schema['headers'] or {},
        'params': 'params' in schema and schema['params'] or {},
    }
    check = get_check(struct)

    @wraps(route)
    def handler():
        params = request.args.to_dict()
        body = request.get_json()
        body = body if body else request.form.to_dict()
        headers = {}
        for i, key in enumerate(request.headers.keys()):
            headers[key] = request.headers.values()[i]
        to_check = {'body': body, 'headers': headers, 'params': params}
        custom = True if 'custom' not in schema else schema['custom'](
            body, headers, params)
        if custom != True:
            response = jsonify({'message': 'Request Error', 'errors': custom})
            response.status_code = 400
            return response
        if check(to_check) == False:
            response = jsonify(
                {'message': 'Request Error', 'errors': check.errors})
            response.status_code = 400
            return response
        result = route()
        if type(result) != dict:
            return result

        response = jsonify(result['body'])
        response.status_code = result['status']
        return response
    return handler


def define_routes(app):
    for file in modules:
        if (isfile(file) and not file.endswith('__init__.py')):
            key = file.split('/')
            key = key[-1]
            key = key[:-3]
            schema = import_module('api.routes.schemas.' + key).schema
            for name in schema.keys():
                route = __import__('api.routes.' + key, fromlist=[name])
                route = getattr(route, name)
                if (callable(route)):
                    app.route(schema[name]['paths'],
                              methods=schema[name]['methods'])(get_handler(schema[name], name, route))
