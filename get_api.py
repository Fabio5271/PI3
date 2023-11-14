import json
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # Desabilitar aviso de SSL

api_url_base = 'https://gtm.delary.dev'
headers = {'Content-Type': 'application/json',
           'accept': 'application/json'}


def get_labrts():
    api_url = f'{api_url_base}/labirintos'
    resp = requests.get(api_url, headers=headers, verify=False)

    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code, json.loads(resp.content.decode('utf-8'))
    

def post_iniciar(id, labirinto):
    api_url = f'{api_url_base}/iniciar'
    pload = ('{' +
             f'"id": "{id}",' +
             f'"labirinto": "{labirinto}"' +
             '}')
    resp = requests.post(api_url, headers=headers, data=pload, verify=False)
    
    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code, json.loads(resp.content.decode('utf-8'))
    

def post_movmt(id, labirinto, nova_pos):
    api_url = f'{api_url_base}/movimentar'
    pload = ('{' +
            f'"id": "{id}",' +
            f'"labirinto": "{labirinto}",' +
            f'"nova_posicao": {nova_pos}' +
            '}')
    resp = requests.post(api_url, headers=headers, data=pload, verify=False)
    
    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code, json.loads(resp.content.decode('utf-8'))


def post_vald(id, labirinto, tds_mov):
    api_url = '{0}/validar_caminho'.format(api_url_base)
    pload = ('{' +
            f'"id": "{id}",' +
            f'"labirinto": "{labirinto}",' +
            f'"todos_movimentos": {tds_mov}' +
            '}')
    resp = requests.post(api_url, headers=headers, data=pload, verify=False)
    
    if resp.status_code == 200:
        return json.loads(resp.content.decode('utf-8'))
    else:
        return resp.status_code, json.loads(resp.content.decode('utf-8'))