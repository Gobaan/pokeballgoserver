import requests
import json

roots = ['http://localhost:7071', 'https://pokemongocatcher.azurewebsites.net']
root = roots[0]
image_file = 'data/zubat.jpg'
files = {'snapshot': open(image_file, 'rb')}
endpoint = f'{root}/api/OCR'
response = requests.post(endpoint, files=files)
print (response)
print (response.text)
pokemon = json.loads(response.text)
print (pokemon)
pokemon['target'] = [32, 24]
endpoint = f'{root}/api/UpdatePokemon'
response = requests.post(endpoint, json=pokemon)
print (response.text)

