from utils import submit_solution, get_problem, ACCESS_TOKEN
import base64
from rdbtools import RdbParser, RdbCallback
from rdbtools.encodehelpers import bytes_to_unicode


PROBLEM_ENDPOINT = f'/challenges/the_redis_one/problem?access_token={ACCESS_TOKEN}'
SOLUTION_ENDPOINT = f'/challenges/the_redis_one/solve?access_token={ACCESS_TOKEN}'

def write_redis_dump(data):
    rdb_data = data['rdb']
    decoded_data = base64.b64decode(rdb_data)
    new_decoded_data = b'REDIS' + decoded_data[5:] # correct the header (first 5 bytes)
    with open('restore.rdb', 'wb') as output_file:
        output_file.write(new_decoded_data)


def is_ascii(data):
    return all(byte < 128 for byte in data)


class CustomParser(RdbCallback):
    def __init__(self):
        super(CustomParser, self).__init__(string_escape=None)
        self.key_value_pairs = []
        self.nested_hashes = {}
        self.db_count_ = 0

    def encode_key(self, key):
        return bytes_to_unicode(key, self._escape, skip_printable=True)

    def encode_value(self, val):
        return bytes_to_unicode(val, self._escape)

    def set(self, key, value, expiry, info):
        if is_ascii(key):
            encoded_key = self.encode_key(key)
        else:
            encoded_key = 'emoji_key_value'
        encoded_value = self.encode_value(value)
        self.key_value_pairs.append((encoded_key, encoded_value, expiry))


    def start_database(self, db_number):
        self.db_count_ += 1

    def start_hash(self, key, length, expiry, info):
        self.current_key = key
        self.nested_hashes[self.encode_key(key)] = {}

    def hset(self, key, field, value):
        self.nested_hashes[self.encode_key(key)][self.encode_key(field)] = self.encode_value(value)

    def end_hash(self, key):
        self.key_value_pairs.append((self.encode_key(key), self.nested_hashes[self.encode_key(key)], None))
        
    def start_list(self, key, expiry, info):
        self.current_list_data = []

    def rpush(self, key, value):
        self.current_list_data.append(self.encode_value(value))

    def end_list(self, key, info):
        encoded_key = self.encode_key(key)
        self.key_value_pairs.append((encoded_key, self.current_list_data, None))

    def start_set(self, key, cardinality, expiry, info):
        self.current_set_data = set()

    def sadd(self, key, member):
        self.current_set_data.add(self.encode_value(member))

    def end_set(self, key):
        encoded_key = self.encode_key(key)
        self.key_value_pairs.append((encoded_key, self.current_set_data, None))

###################################### MAIN ######################################
'''
The crux of this exercise was using a redis parser to get the data and metadata out of the redis dump
The callbacks in the parser are called upon encountering the specific data structures in the redis dump, hence we
can rewrite them for our purpose of extracting value out of certain datastructures.

Also datetime obj gives timestamp -5.5hrs to adjust for UTC, took some time debugging and fixing that.
parser reference -> https://github.com/sripathikrishnan/redis-rdb-tools/blob/master/rdbtools/parser.py
'''
data = get_problem(PROBLEM_ENDPOINT)
write_redis_dump(data)
special_key = data['requirements']['check_type_of'] 

rdb_file_path = "restore.rdb"
callback = CustomParser()
parser = RdbParser(callback)
parser.parse(rdb_file_path)

# CREATE THE SOLUTION JSON
solution = {}
for key, value, expiry in callback.key_value_pairs:
    if expiry is not None:
        timestamp_ms = int(expiry.timestamp() * 1000) + 19800000 # shifting to UTC, +5.5hrs
        solution['expiry_millis'] = timestamp_ms

    if key == special_key:
        if isinstance(value, list):
            solution[special_key] = 'list'
        elif isinstance(value, dict):
            solution[special_key] = 'hash'
        elif isinstance(value, set):
            solution[special_key] = 'set'
            
    if key == 'emoji_key_value':
        solution['emoji_key_value'] = value


solution['db_count'] = callback.db_count_

submit_solution(solution,SOLUTION_ENDPOINT)

