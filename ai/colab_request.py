import requests

def generate(query):
    url = 'https://f6a6-34-125-86-9.ngrok-free.app/'
    r = requests.post(url + 'generate', json = {'query': query})
    print('Colab request status', r.status_code)
    if r.status_code == 200:
        return r.json()['response']
    else:
        return "Could not generate response"