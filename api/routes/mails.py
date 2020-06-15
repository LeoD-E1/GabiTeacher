from cerberus import Validator as get_check
from os.path import isdir
from flask import render_template
from glob import glob
from importlib import import_module

from api.commons.mails import send
from api.commons.root_dir import root_dir

# templates_namespace = 'templates.mails'
# templates_path = root_dir + '/' + '/'.join(templates_path.split('.'))
# template_dirs = glob(templates_namespace + '/*')
# templates = {}
# for tdir in template_dirs:
#     if (not isdir(tdir)):
#         continue
#     tdir = tdir.split('/')
#     tdir = tdir[-1]
#     print('tdir')
#     print(tdir)
#     template = {}
#     template['spec'] = import_module(
#         templates_path + '.' + tdir + '.spec').spec
#     template['html'] = render_template()


def send_email(req):
    to = req['body']['to']
    to = [to] if type(to) == str else to
    subject = req['body']['subject']
    text = req['body']['text']
    html = req['body']['html']
    result = send(to, subject, text, html)
    return {'status': 200, 'body': result}


def send_email_template(req):
    to = req['body']['to']
    to = [to] if type(to) == str else to
    subject = req['body']['subject']
    text = req['body']['text']
    html = req['body']['html']
    result = send(to, subject, text, html)
    return {'status': 200, 'body': result}
