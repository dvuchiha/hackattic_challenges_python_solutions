from utils import submit_solution, get_problem
import base64
import hashlib
import hmac
import binascii
import scrypt


PROBLEM_ENDPOINT = '/challenges/password_hashing/problem?access_token=b5f0878f05fe56ea'
SOLUTION_ENDPOINT = '/challenges/password_hashing/solve?access_token=b5f0878f05fe56ea'


def calculate_sha256_hash(password):
    sha256_hash = hashlib.sha256(password).hexdigest()
    return sha256_hash

def generate_hmac(password, salt, hash_function=hashlib.sha256):
    hmac_result = hmac.new(key=salt, msg=password, digestmod=hash_function).hexdigest()
    return hmac_result

def generate_pbkdf2(password, salt, iterations, hash_function):
    pbkdf2_hash = hashlib.pbkdf2_hmac(hash_function, password, salt, iterations)
    return binascii.hexlify(pbkdf2_hash).decode('utf-8')

def generate_scrypt(password, salt, iterations, r, p, buflen):
    hashed = scrypt.hash(password = password, 
                       salt = salt, 
                       N = iterations, 
                       r = r, 
                       p = p, 
                       buflen = buflen)
    
    return hashed.hex()


# main
'''
CRUX OF THE EXERCISE : 
Internally, scrypt uses PBKDF2-with-a-low-number-of-rounds as a building block (adds memory_intensiveness),
with PBKDF2 using the HMAC construction (adds time_intensiveness),
with HMAC using a (typically Merkle-Damgård) hash such as (typically) SHA-256 (does XOR operations on salt/key and hashes that resultant + password)
 & SHA-256 IS A PSEUDORANDOM CRYPTOGRAPHIC FUNCTION
'''

data = get_problem(PROBLEM_ENDPOINT)

password = data['password'].encode('utf-8') # to bytes
salt = base64.b64decode(data['salt'])

solution = {}

solution['sha256'] = calculate_sha256_hash(password)
solution['hmac'] = generate_hmac(password, salt)
solution['pbkdf2'] = generate_pbkdf2(password, salt, data['pbkdf2']['rounds'], data['pbkdf2']['hash'])
solution['scrypt'] = generate_scrypt(password, salt, data['scrypt']['N'], data['scrypt']['r'], data['scrypt']['p'], data['scrypt']['buflen'])

submit_solution(solution, SOLUTION_ENDPOINT)




