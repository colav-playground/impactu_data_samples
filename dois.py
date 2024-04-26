import pandas as pd
import json
from time import sleep
import requests 

dois = requests.get( 'https://raw.githubusercontent.com/colav-playground/impactu_data_samples/main/dois-scienti.json')

dois = [ x.lower() for x in dois.json() if x is not None]

DOIS = []
for doi in dois:
    d={}
    print(doi)
    j = requests.get(f'https://api.openalex.org/works/https://doi.org/{doi}')
    if j.status_code == 200 and j.json():
        print('found!')
        d['doi'] = doi
        d['OpenAlex'] = j.json().get('id')
    if d:
        DOIS.append(d)
    sleep(0.1)

f = open('dois_scienti_found_in_OpenAlex.json','w')
json.dump(DOIS,f)
f.close()
