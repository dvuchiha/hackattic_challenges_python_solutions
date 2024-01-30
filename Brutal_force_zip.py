from utils import submit_solution, get_problem, ACCESS_TOKEN
import requests
import subprocess
import re
import zipfile

PROBLEM_ENDPOINT = f'/challenges/brute_force_zip/problem?access_token={ACCESS_TOKEN}'
SOLUTION_ENDPOINT = f'/challenges/brute_force_zip/solve?access_token={ACCESS_TOKEN}'

def fetch_psw_from_terminal_output(output):
    pattern = re.compile(r"\n([a-zA-Z0-9]+)\s+\(zip_file\.zip\)")
    match_ = re.search(pattern, output)
    return match_.group(1) if match_ else ''

def download_zip(url, save_path):
    response = requests.get(url, stream=True)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=512):
                file.write(chunk)
        print(f"ZIP file downloaded successfully and saved at: {save_path}")
    else:
        print(f"Failed to download ZIP file. Status code: {response.status_code}")

def run_subprocess(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output.decode('utf-8').strip(), error.decode('utf-8').strip()
    except Exception as e:
        print(f"Error running subprocess command: {command}. Error: {e}")
        return '', ''

# MAIN

'''
The total number of all possible passwords are ~ 3 billion {exponential -> charset^length}, 
hence simple Brute force wouldn't work with consumer hardware.
We will apply the hack of using the open-source JohnTheRipper library, which uses multiple hacks like 
- Incremental mode, huge rainbow tables, checksum comparisons etc. to reduce the search space and perform
a calculated & optimized brute force attack.
'''

try:
    data = get_problem(PROBLEM_ENDPOINT)        
    save_path = 'zip_file.zip'
    target_file = 'secret.txt'
    download_zip(data['zip_url'], save_path)

    # non-brute hacking

    # Command to run zip2john and generate hash
    zip2john_command = "/opt/homebrew/Cellar/john-jumbo/1.9.0_1/share/john/zip2john zip_file.zip > zip.hash"
    output_zip2john, _ = run_subprocess(zip2john_command) # we receive a non-fatal error due to multiple files present in the zip

    # Command to run john on the generated hash with incremental mode specified according to password constraints.
    john_command = "john --incremental=LowerNum zip.hash"
    output_john, _ = run_subprocess(john_command)

    # Extract the cracked password from the John output
    cracked_string = output_john.strip()

    password = fetch_psw_from_terminal_output(cracked_string)

    # SEND THE RESPONSE
    with zipfile.ZipFile(save_path, 'r') as zip_file:
        zip_file.setpassword(bytes(password, 'utf-8'))
        solution = {}
        with zip_file.open(target_file) as target_file_contents:
            solution['secret'] = target_file_contents.read().decode('utf-8').strip()
            submit_solution(solution, SOLUTION_ENDPOINT)

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # remove zip file/folders
    remove_command = "rm -rf zip*"
    run_subprocess(remove_command)


