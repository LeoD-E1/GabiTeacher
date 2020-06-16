schema = {
    'send_email': {
        'paths': '/api/mail',
        'methods': ['POST'],
        'body': {
            'to': {'required': True, 'type': ['string', 'list']},
            'subject': {'required': True, 'type': 'string'},
            'html': {'required': True, 'type': 'string'},
            'text': {'required': True, 'type': 'string'}
        }
    },
    'send_email_template': {
        'paths': '/api/mail/<template_name>',
        'methods': ['POST'],
        'body': {
            'to': {'required': True, 'type': ['string', 'list']},
            'subject': {'required': True, 'type': 'string'},
            'data': {'required': True, 'type': 'dict'}
        },
        'params': {
            'template_name': {'required': True, 'type': 'string'}
        }
    }
}
