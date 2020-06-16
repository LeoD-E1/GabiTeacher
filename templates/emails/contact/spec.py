from constants import EMAIL_REGEX

spec = {
    'name': {'required': True, 'type': 'string'},
    'email': {'required': True, 'regex': EMAIL_REGEX},
    'message': {'required': True, 'type': 'string'}
}
