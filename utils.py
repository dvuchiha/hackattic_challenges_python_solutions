import requests
DOMAIN = 'https://hackattic.com'

def submit_solution(input_data, url):
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=input_data, timeout=20)
        response.raise_for_status()
        
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Body:", response.text)
        
    except requests.exceptions.RequestException as e:
        print("Couldn't do POST:", e)