import requests
import json

DOMAIN = 'https://hackattic.com'

def submit_solution(input_data, url):
    headers = {'Content-Type': 'application/json'}
    solution_url = DOMAIN + url
    try:
        response = requests.post(solution_url, headers=headers, json=input_data, timeout=20)
        response.raise_for_status()
        
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Body:", response.text)
        
    except requests.exceptions.RequestException as e:
        print("Couldn't do POST:", e)

def get_problem(url):
    problem_url = DOMAIN + url
    try:
        response = requests.get(problem_url)
        response.raise_for_status()
        
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Body:", response.text)
    except requests.exceptions.RequestException as e:
        print("Couldn't do GET:", e)

    json_string = response.content.decode('utf-8') # binary to string
    result_dict = json.loads(json_string) # string to dict

    return result_dict