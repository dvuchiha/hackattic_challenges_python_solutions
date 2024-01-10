from utils import submit_solution, get_problem
import base64
import io
import gzip
import csv
import subprocess

def read_csv_to_list(file_path):
    data_list = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_list.append(row['ssn'])

    return data_list

PROBLEM_ENDPOINT = '/challenges/backup_restore/problem?access_token=b5f0878f05fe56ea'
SOLUTION_ENDPOINT = '/challenges/backup_restore/solve?access_token=b5f0878f05fe56ea'

data = get_problem(PROBLEM_ENDPOINT)
dump = data['dump']

# Decode the base64 string
decoded_data = base64.b64decode(dump)

# Decompress the data using gzip
with gzip.GzipFile(fileobj=io.BytesIO(decoded_data), mode='rb') as f:
    decompressed_data = f.read()

# Write the decompressed data to a file
with open('restore.sql', 'wb') as output_file:
    output_file.write(decompressed_data)


'''
Database was created separately using psql 
'''
restore_command = "psql mydatabase < restore.sql"
export_command = """psql -c "\COPY (SELECT ssn FROM criminal_records where status='alive') TO 'alive_ssns.csv' WITH CSV HEADER;" mydatabase"""
drop_table_command = "psql -c 'DROP TABLE IF EXISTS criminal_records;' mydatabase"

try:

    # Restore the dump to the database
    subprocess.run(restore_command, shell=True, check=True)

    # Export data to CSV
    subprocess.run(export_command, shell=True, check=True)

    # drop table for consequent runs
    subprocess.run(drop_table_command, shell=True, check=True)

except subprocess.CalledProcessError as e:
    print(f"Error: {e}")


# Specify the path to your CSV file
csv_file_path = 'alive_ssns.csv'

# Call the function to read the CSV file and store data in a list
csv_data_list = read_csv_to_list(csv_file_path)

solution = {'alive_ssns':csv_data_list}

submit_solution(solution,SOLUTION_ENDPOINT)

