#!/usr/bin/python3

import sys
import time
import json
import requests

#MB/22andme DO API Library
#OOO:
#0: User goes through purple to pay set amount, then gets URL for entrypoint webui
#1: User inputs PubKeyName and PubKey at entrypoint webui
#2: Upload pubkey info to DO API Burner Account for that day/week (depends on op tempo)
#3: After successful keymat upload, Builds Droplet with the same name as the PubKeyName
#4: Returns basic info about the droplet to the user, entrypoint provides phpshell (for tails users)
#5: Runs timer (displayed to user), at zero deletes droplet and ssh-key, nukes webui too

#cut keys: ssh-keygen -f ./frongleberries -t ecdsa -b 521
#copy paste or do a open(realline(str(frongleberries))) for the var

#PROTECT THE BEARER, OPSEC!
apitoken = 'hahaimnotthattired'
apiurl = 'https://api.digitalocean.com'
report = ['DO account stats', '  ', '  ']
burntag = "test"

def superdangerburnbytag(burntag):
        apiendpoint = apiurl + '/v2/droplets?tag_name=' + burntag
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.delete(apiendpoint, headers=headerboi)
        print("DELETE BY TAG FUNCTION RAN - CHECK THE WEBUI TO VERIFY DELETION!")

def checkkeymat():
        allkeys = {}
        apiendpoint = apiurl + '/v2/account/keys'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        req = requests.get(apiendpoint, headers=headerboi)
        jason = req.json()
        for keymat in jason['ssh_keys']:
                thisname = str(keymat['name'])
                thisid = str(keymat['id'])
                allkeys.update({thisname : thisid})
        return allkeys

def checkkeymatbyid(keyid):
        #Returns name of given key id
        thiskeymat = checkkeymat()
        for name,id in thiskeymat.items():
                if id == keyid:
                        print(name)
                        return name

def checkkeymatbyname(keyname):
        #Returns id of given key name
        thiskeymat = checkkeymat()
        for name,id in thiskeymat.items():
                if name == keyname:
                        print(id)
                        return int(id)

def uploadkeymat(keyname,pubstring):
        apiendpoint = apiurl + '/v2/account/keys'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        databoi = {'name': '{}'.format(keyname), 'public_key': '{}'.format(pubstring) }
        req = requests.post(apiendpoint, json=databoi, headers=headerboi)
        jason = req.json()
        try:
                pubkeyname = str(jason['ssh_key']['name'])
                pubkeyid = str(jason['ssh_key']['id'])
                print("Successfully uploaded pubkey '" + pubkeyname + "' at ID#: " + pubkeyid)
                return pubkeyid
        except:
                print("PubKey upload failed, pubkey may already exist...")

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
        #DEPENDS ON NAME OF PUBKEY, PUBKEY MUST BE UPLOADED FIRST, combine the funcs dummy
        #Generates a droplet with given args above
        thesetags = [burntag]
        regionandsize = checkregions(region, size)
        apiendpoint = apiurl + '/v2/droplets'
        headerboi =  {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(apitoken)}
        databoi = {'name': '{}'.format(name), 'tags': thesetags, 'region': '{}'.format(regionandsize[0]), 'size': '{}'.format(regionandsize[1]), 'image': '{}'.format(image), 'ssh_keys': ['{}'.format(int(checkkeymatbyname(name)))]}
        req = requests.post(apiendpoint, json=databoi, headers=headerboi)
        jason = req.json()
        did = str(jason['droplet']['id'])
        print("Created a droplet with ID:" + did)
        print("Waiting for provisioning...")
        #needs to have a 1+ second for throttling
        time.sleep(7)
#       checkdroplet(did)

def checkdroplet(did):
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





#debug junk below
count = 48;
for i in range(count):
        try:
                createdroplet("worker","nyc1","1gb", "ubuntu-16-04-x64")
        except Exception as err:
                print("nope  -  " + str(err))


#uploadkeymat('worker','ecdsa-sha2-nistp521 noway0099 root')

#superdangerburnbytag(burntag)
