from cerberus import Validator as get_check
from os.path import isdir, basename
from flask import render_template
from glob import glob
from importlib import import_module

from api.commons.emails import send
from api.commons.root_dir import root_dir
from api.commons.env import env

_domain = env.get('MAILGUN_DOMAIN')
_user = env.get('MAIL_USER')

_templates_namespace = 'templates.emails'
_templates_path = root_dir + '/' + '/'.join(_templates_namespace.split('.'))
_template_dirs = glob(f'{_templates_path}/*')
templates = {}
for tdir in _template_dirs:
    if (not isdir(tdir)):
        continue
    name = basename(tdir)
    template = {}
    spec = import_module(f'{_templates_namespace}.{name}.spec').spec
    preview_data = import_module(
        f'{_templates_namespace}.{name}.preview_data').preview_data
    template['html_path'] = f'emails/{name}/html.html'
    template['text_path'] = f'emails/{name}/text.txt'
    template['preview_data'] = preview_data
    template['check'] = get_check(spec)
    templates[name] = template


def _get_email(body):
    from_email = f'{_user}@{_domain}'
    if 'from_email' in body:
        if 'from_name' in body:
            from_email = f"{body['from_name']} <{body['from_email']}>"
        else:
            from_email = body['from_email']
    return from_email


def send_email(req):
    to = req['body']['to']
    to = [to] if type(to) == str else to
    subject = req['body']['subject']
    text = req['body']['text']
    html = req['body']['html']
    from_email = _get_email(req['body'])
    return send(from_email, to, subject, text, html)


def send_email_template(req):
    name = req['params']['template_name']
    if (name not in templates):
        return {'status': 404, 'body': {'message': f"Template '{name}' not found"}}
    template = templates[name]
    to = req['body']['to']
    to = [to] if type(to) == str else to
    subject = req['body']['subject']
    data = req['body']['data']
    check = template['check']
    if (not check(data)):
        return {'status': 400, 'body': {'message': f"Invalid Data for template '{name}'", 'errors': check.errors}}
    html = render_template(template['html_path'], data=data)
    text = render_template(template['text_path'], data=data)
    from_email = _get_email(req['body'])
    return send(from_email, to, subject, text, html)


def preview_email_template(req):
    name = req['params']['template_name']
    view = req['params']['view']
    if name not in templates:
        return {'status': 404, 'body': {'message': f"Template '{name}' not found"}}
    template = templates[name]
    data = template['preview_data']
    if view == 'html':
        return render_template(template['html_path'], data=data)
    elif view == 'text':
        return render_template(template['text_path'], data=data)
