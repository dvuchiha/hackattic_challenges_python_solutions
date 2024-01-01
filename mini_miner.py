import hashlib
import json
from utils import submit_solution, get_problem


PROBLEM_ENDPOINT = '/challenges/mini_miner/problem?access_token=b5f0878f05fe56ea'
SOLUTION_ENDPOINT = '/challenges/mini_miner/solve?access_token=b5f0878f05fe56ea'

def calculate_sha256_hash(data,difficulty):
    sha256_hash = hashlib.sha256()
    
    data  = json.dumps(data, sort_keys=True, separators=(',', ':')) # serialize & no whitespace

    data = data.encode('utf-8')  # convert to bytes obj

    sha256_hash.update(data)

    # Get the hexadecimal representation of the hash
    hashed_value = sha256_hash.hexdigest()

    # get 256-bit binary digest
    digest = sha256_hash.digest()
    hashed_binary = ''.join(format(byte, '08b') for byte in digest)
    
    return (True, hashed_binary,hashed_value) if hashed_binary[:difficulty] == '0'*difficulty else (False, hashed_binary,hashed_value)

data = get_problem(PROBLEM_ENDPOINT)

# how mining works is basically we try all possible values of nonce to get hash
# starting with specified number of zero-bits.

# Brute force the 32-bit/4-byte nonce
solution = {'data':data['block']['data']}
difficulty = data['difficulty']
for i in range(2**32):
    solution['nonce'] = i
    mined, hash_result, hashed_value = calculate_sha256_hash(solution,difficulty)
    if mined:
        print(hash_result)
        print(hashed_value)
        submit_solution({'nonce':i}, SOLUTION_ENDPOINT)
        print("Successfully mined with nonce",i)
        break
    

'''
Time complexity => ~ O(2^difficulty), becoz we need zeros in the first 'difficulty' positions of the 
binary hash and there are always 2 options (1 or 0), 
there is a (1 / 2^diffculty) probability of finding the nonce that creates such hash.
Note - We ignore the time taken by sha2 algo but it's directly proportional to the length of 
input-data.

Space complexity => O(1)
'''


