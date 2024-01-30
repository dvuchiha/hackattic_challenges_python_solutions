from utils import submit_solution, get_problem, ACCESS_TOKEN
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography import x509
import datetime


'''
Self-signed as we use the same key to create CSR request and same key to sign it.

To create a Self-signed certificate, follow these steps
(To perform below steps we'll need openssl)
1. create RSA KEY (this is provided)
2. create CSR req using the key
3. sign the request using RSA_key and create the certificate
'''

PROBLEM_ENDPOINT = f'/challenges/tales_of_ssl/problem?access_token={ACCESS_TOKEN}'
SOLUTION_ENDPOINT = f'/challenges/tales_of_ssl/solve?access_token={ACCESS_TOKEN}'


data = get_problem(PROBLEM_ENDPOINT)

RSA_key = data['private_key']
domain = data['required_data']['domain']
serial_number = int(data['required_data']['serial_number'], 0)
country_code = 'US'

key = serialization.load_der_private_key(base64.b64decode(RSA_key), password=None)

subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, country_code),
    x509.NameAttribute(NameOID.COMMON_NAME, domain),
])

cert = x509.CertificateBuilder() \
    .subject_name(subject) \
    .issuer_name(subject) \
    .public_key(key.public_key()) \
    .serial_number(serial_number) \
    .not_valid_before(datetime.datetime.utcnow()) \
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)) \
    .sign(key, hashes.SHA256())

solution = {
    'certificate': base64.b64encode(cert.public_bytes(serialization.Encoding.DER)).decode('utf-8')
}


submit_solution(solution,SOLUTION_ENDPOINT)

