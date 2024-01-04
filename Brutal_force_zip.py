from utils import submit_solution, get_problem
import requests


PROBLEM_ENDPOINT = '/challenges/brute_force_zip/problem?access_token=b5f0878f05fe56ea'
SOLUTION_ENDPOINT = '/challenges/brute_force_zip/solve?access_token=b5f0878f05fe56ea'


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



# main
data = get_problem(PROBLEM_ENDPOINT)        
save_path = 'zip_file.zip'
print(download_zip(data['zip_url'], save_path))

'''
The total number of all possible passwords are ~ 3 billion {exponential -> charset^length}, 
hence simple Brute force wouldn't work with consumer hardware.
We will apply the hack of using the widely available 'rockyou.txt' file / some library
'''
