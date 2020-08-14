#!/usr/bin/python3

import json
import requests

apitoken = 'hahayeahright'
apiurl = 'https://api.digitalocean.com'
report = ['DO account stats', '  ', '  ']
regions = {}

def getregions():
        apiendpoint = apiurl + '/v2/regions'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.get(apiendpoint, headers=headerboi)
        jason = req.json()
        for region in jason['regions']:
                regions.update({str(region['slug']): region['sizes']})

def createdroplet(name, region, size, image):
        apiendpoint = apiurl + '/v2/droplets'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        databoi = {'name': '{}'.format(name), 'region': '{}'.format(region), 'size': '{}'.format(size), 'image': '{}'.format(image)}
        req = requests.post(apiendpoint, json=databoi, headers=headerboi)
        jason = req.json()
        print(jason)

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


#getregions()
#print(regions['nyc1'])
#createdroplet("brongletest","sfo2","s-1vcpu-1gb", "ubuntu-16-04-x64")
#checkbalance()
#checkdroplets()
#for i in report:
#       print(i)
