#!/usr/bin/python3

import json
import pprint
import requests

apitoken = 'SuperNiftyAPItoken'
apiurl = 'https://api.digitalocean.com'
report = ['DO account stats', '  ', '  ']

def checkdroplets():
        apiendpoint = apiurl + '/v2/droplets'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.get(apiendpoint, headers=headerboi)
        jason = req.json()
        report.append("--VPS List--")
        for names in jason['droplets']:
                report.append("Name: " + str(names['name']))
                report.append("Size: " + str(names['size_slug']))
                report.append("WANip: " +str(names['networks']['v4'][0]['ip_address']))
                report.append("Status: " + str(names['status']) + " ///  Region: " + str(names['region']['slug']))
                report.append(str(" --- "))

def checkbalance():
        apiendpoint = apiurl + '/v2/customers/my/balance'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.get(apiendpoint, headers=headerboi)
        jason = req.json()
        report.append(str("Current balance due: " + jason['month_to_date_usage']))
        report.append(str("This report was generated on: " +jason['generated_at']))


checkbalance()
checkdroplets()
for index in report:
        print(index)
