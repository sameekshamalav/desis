# import json
# from datetime import datetime, timedelta, timezone
# from jwt import JWT, jwk_from_dict
# from jwt.utils import get_int_from_datetime
# from .models import User  # Import your User model here

# instance = JWT()

# def generate_jwt_token(user):
#     message = {
#         'iss': 'https://example.com/',
#         'sub': str(user.user_id),
#         'user_name': user.user_name,
#         'iat': get_int_from_datetime(datetime.now(timezone.utc)),
#         # 'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(None)),
#         # Add more user information as needed
#     }

#     # Load a RSA key from a PEM file or any other suitable method
#     with open('rsa_private_key.pem', 'rb') as fh:
#         signing_key = jwk_from_pem(fh.read())

#     # Encode the message to JWT(JWS)
#     compact_jws = instance.encode(message, signing_key, alg='RS256')
#     return compact_jws

# def decode_jwt_token(token):
#     with open('rsa_public_key.json', 'r') as fh:
#         verifying_key = jwk_from_dict(json.load(fh))

#     message_received = instance.decode(token, verifying_key, do_time_check=True)
#     return message_received


import datetime
from jwt import JWT, jwk_from_dict
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from jwt.utils import get_int_from_datetime
instance = JWT()

def generate_jwt_token(user):
    message = {
        'iss': 'https://example.com/',
        'sub': str(user.user_id),
        'user_name': user.user_name,
        'iat': get_int_from_datetime(datetime.now(datetime.timezone.utc)),
        'exp': get_int_from_datetime(datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)),
        # Add more user information as needed
    }

    # Load a RSA private key from a PEM file
    with open('rsa_private_key.pem', 'rb') as fh:
        private_key_data = fh.read()
        private_key = load_pem_private_key(private_key_data, password=None)

    # Extract the JWK from the private key
    signing_key = jwk_from_dict({
        "kty": "RSA",
        "kid": "your-key-id",
        "use": "sig",
        "n": private_key.public_key().public_numbers().n,
        "e": private_key.public_key().public_numbers().e,
    })

    # Encode the message to JWT(JWS)
    compact_jws = instance.encode(message, signing_key, alg='RS256')
    return compact_jws
