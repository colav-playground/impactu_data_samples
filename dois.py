import pandas as pd
import json
from time import sleep
import requests 
from re import sub
from re import search

dois = requests.get( 'https://raw.githubusercontent.com/colav-playground/impactu_data_samples/main/dois-scienti.json').json()
print(len(dois))

dois = [x.strip().split()[0] for x in dois if x is not None and x.strip()]
dois = [ x.lower() for x in dois if x is not None]
dois = [sub('^https*:\/\/[\w\.0-9]+\/','',x) for x in dois]
dois = [sub('^doi\:\s*','',x) for x in dois ]
dois = [ x for x in dois if search('^10\.',x) ]
print(len(dois))

DOIS = []
i=0
for doi in dois:
    d={}
    j = requests.get(f'https://api.openalex.org/works/https://doi.org/{doi}')
    i += 1
    if j.status_code == 200 and j.json():
        print(f'found! {doi}'.ljust(100),end='\r')
        d['doi'] = doi
        d['OpenAlex'] = j.json().get('id')
        d['OA_doi'] = j.json().get('doi')
    if d:
        DOIS.append(d)
        if doi.lower() != j.json().get('doi').replace('https://doi.org/','').lower():
            print(f'Not found {doi}')
            break
    sleep(0.1)
    #break

f = open('dois_scienti_found_in_OpenAlex.json','w')
json.dump(DOIS,f)
f.close()