from functools import wraps
from importlib import import_module
from cerberus import Validator as check
from os.path import dirname, basename, isfile, join
from flask import request
from json import dumps
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))


def get_handler(schema, name, route):
    struct = {
        'body': 'body' in schema and schema['body'] or {},
        'headers': 'headers' in schema and schema['headers'] or {},
        'params': 'params' in schema and schema['params'] or {},
    }

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
            body, headers)
        return route() if custom and check(struct)(to_check) else 'Pusiste cualquier cosa flaco'
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
