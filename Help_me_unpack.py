import requests
import json
import base64
import struct
from utils import submit_solution, DOMAIN


problem_endpoint = '/challenges/help_me_unpack/problem?access_token=b5f0878f05fe56ea'
problem_url = DOMAIN + problem_endpoint

resp = requests.get(problem_url)
json_string = resp.content.decode('utf-8') # binary to string
result_dict = json.loads(json_string) # string to dict

'''
TO solve this , we follow 2 step process
Decode the base64-encoded string to obtain the binary data.
convert binary -> decimal based on heuristics {get specific byte chunks and convert}
'''

# Decode the Base64 data back to binary
decoded_data = base64.b64decode(result_dict['bytes']) #base64 to binary

solution = {}
# a regular int (signed), to start off
solution['int'] = struct.unpack('<i',decoded_data[0:4])[0]
# an unsigned int
solution['uint'] = struct.unpack('<I',decoded_data[4:8])[0]
# a short (signed) to make things interesting
solution['short'] = struct.unpack('<hxx',decoded_data[8:12])[0]
# a float because floating point is important
solution['float'] = struct.unpack('<f',decoded_data[12:16])[0]
# a double as well
solution['double'] = struct.unpack('<d',decoded_data[16:24])[0]
# another double but this time in big endian (network byte order)
solution['big_endian_double'] = struct.unpack('>d',decoded_data[24:32])[0]

print(solution)

solution_endpoint = '/challenges/help_me_unpack/solve?access_token=b5f0878f05fe56ea'
solution_url = DOMAIN + solution_endpoint
submit_solution(solution, solution_url)

