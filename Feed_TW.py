#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import subprocess
from multiprocessing.pool import ThreadPool
PoolConex2=ThreadPool(processes=600)

def requests_retry_session(
        retries=100,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
    ):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def tomar2(url):
    r=requests_retry_session().get(url, timeout=2)
    return r.text

def GuardarJsonTwitterCVE(json_TW):
    with open('json_twitter.json', 'w') as file:
        json.dump(json_TW, file)

def ObtenerJsonURLTw():
    url="http://porsilapongo.cl/API_MOD/TwitterJSON.php?options=7"
    r=PoolConex2.apply_async(tomar2,([url]))
    svr=r.get()
    return svr

def ObtenerJsonTwitterCVE():
    with open('json_twitter.json', 'r') as file:
        data = json.load(file)
        return data

def EnviarCVETwitter():
    try:
        JSON_DOC=json.dumps(ObtenerJsonTwitterCVE())
        JSON_URL=json.dumps(ObtenerJsonURLTw())
        DATA_URL=json.loads(JSON_URL)
        DATA_DOC=json.loads(JSON_DOC)
        if DATA_DOC[0]['id_str'] == DATA_URL[0]['id_str']:
                #print(colored('[INFO]Sin Cambios.', 'green', 'on_blue'))
            print ("Sin Cambios")
        else:
                #print(colored('[INFO]Con Cambios.', 'green', 'on_blue'))
            JSON_URL=ObtenerJsonURLTw()
            DATA_URL=json.loads(JSON_URL)
            GuardarJsonTwitterCVE(DATA_URL)
            BD=DATA_URL
            INFO="Mr.Theblood Notify"
            for sh in range(0,4):
                INFO+="Titulo:" + BD[sh]['text'] + "\n"
                INFO+="Fecha:" + BD[sh]['created_at'] + "\n"
                INFO+="----\n"
                #driver.send_message_to_id('56992040705-1542121544@g.us',INFO)
            print (INFO.encode('utf-8'))

    except:
        JSON_URL=ObtenerJsonURLTw()
        DATA_URL=json.loads(JSON_URL)
        GuardarJsonTwitterCVE(DATA_URL)
        BD=DATA_URL
        INFO="Mr.Theblood Notify"
        for sh in range(0,4):
            INFO+="Titulo:" + BD[sh]['text'] + "\n"
            INFO+="Fecha:" + BD[sh]['created_at'] + "\n"
            INFO+="----\n"
        #driver.send_message_to_id('56992040705-1542121544@g.us',INFO)
        print (INFO.encode('utf-8'))


EnviarCVETwitter()
