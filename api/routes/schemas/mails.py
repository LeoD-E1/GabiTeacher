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
    }
}
