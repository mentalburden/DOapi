#!/usr/bin/python3

import time
import json
import requests

apitoken = 'nowayjose'
apiurl = 'https://api.digitalocean.com'
report = ['DO account stats', '  ', '  ']

def getregions():
        #returns a dict of valid regions and size
        theseregions = {}
        apiendpoint = apiurl + '/v2/regions'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.get(apiendpoint, headers=headerboi)
        jason = req.json()
        for region in jason['regions']:
                theseregions.update({str(region['slug']): region['sizes']})
        return theseregions

def checkregions(region, size):
        #returns an array of region and size if valid and available
        validregions = []
        funcregions = getregions()
        for i in funcregions:
                validregions.append(i)
        for thisregion in funcregions:
                if region in thisregion:
                        if size in funcregions[region]:
                                print(size + " and " + region + " are region params valid.")
                                return [region, size]
                        else:
                                print(size + " is not valid, try one of these:")
                                for index in funcregions[region]:
                                        print(index)
                else:
                        print(region + " is not valid, try one of these:")
                        for babyregion in validregions:
                                print(babyregion)
                        break

def createdroplet(name, region, size, image):
        #Begin droplet provisioning, then handover to checkdroplet() to get IP and stats
        regionandsize = checkregions(region, size)
        apiendpoint = apiurl + '/v2/droplets'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        databoi = {'name': '{}'.format(name), 'region': '{}'.format(regionandsize[0]), 'size': '{}'.format(regionandsize[1]), 'image': '{}'.format(image)}
        req = requests.post(apiendpoint, json=databoi, headers=headerboi)
        jason = req.json()
        did = str(jason['droplet']['id'])
        print("Created a droplet with ID:" + did)
        print("Waiting for provisioning...")
        time.sleep(15)
        checkdroplet(did)

def checkdroplet(did):
        #Check droplet by id
        apiendpoint = apiurl + '/v2/droplets/' + did
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.get(apiendpoint, headers=headerboi)
        jason = req.json()
        thisipv4 = str(jason['droplet']['networks']['v4'][0]['ip_address'])
        thisname = str(jason['droplet']['name'])
        thisram = str(jason['droplet']['memory'])
        thiscpu = str(jason['droplet']['vcpus'])
        thisdisk = str(jason['droplet']['disk'])
#       thisipv6 = jason['droplet']['networks']['v6'][0]['ip_address']
        print("A Droplet called '" + thisname + "' is now available on   -  " + thisipv4)
        print("This droplet has " + thiscpu + "vcpus, " + thisram + "ram, and " + thisdisk + "GB of disk.")

def checkdroplets():
        #Check all droplets on account
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
        #Get current monthly billing info
        apiendpoint = apiurl + '/v2/customers/my/balance'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.get(apiendpoint, headers=headerboi)
        jason = req.json()
        report.append(str("Current balance due: " + jason['month_to_date_usage']))
        report.append(str("This report was generated on: " +jason['generated_at']))


#checkregions('nyc1','1gb')
#checkregions('bunchajunk','200000GB')
#getregions()
#print(regions['nyc1'])
#createdroplet("brongletest","nyc1","1gb", "ubuntu-16-04-x64")
#checkbalance()
#checkdroplets()
#for i in report:
#       print(i)

