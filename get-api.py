import json
import requests

api_url_base = 'http://gtm.localhost'
headers = {'Content-Type': 'application/json',
           'accept': 'application/json'}

def get_labrts():
    api_url = '{0}/labirintos'.format(api_url_base)
    resp = requests.get(api_url, headers=headers)

    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code
    
def post_iniciar():
    api_url = '{0}/iniciar'.format(api_url_base)
    pload = ('{"id": "1",'
             '"labirinto": "1"}')
    resp = requests.post(api_url, headers=headers, data=pload)
    
    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code, json.loads(resp.content.decode('utf-8'))
    
def post_movmt():
    api_url = '{0}/movimentar'.format(api_url_base)
    pload = ('{"id": "string",'
            '"labirinto": "string",'
            '"nova_posicao": 0}')
    resp = requests.post(api_url, headers=headers, data=str(pload))
    
    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code, json.loads(resp.content.decode('utf-8'))

def post_vald():
    api_url = '{0}/validar_caminho'.format(api_url_base)
    pload = ('{"id": "string",'
            '"labirinto": "string",'
            '"todos_movimentos": [0]}')
    resp = requests.post(api_url, headers=headers, data=pload)
    
    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code, json.loads(resp.content.decode('utf-8'))
   
print(get_labrts())
print(post_iniciar())
print(post_movmt())
print(post_vald())