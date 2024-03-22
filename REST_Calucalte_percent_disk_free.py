#This script queries vcenter for the list of VMs, gathers their disk usage info
#and calculates the percentage free.  The final part of the script sorts from least to
#greatest amount of space free

import requests
import json
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Do not automate the fetching of a session key.  

#Get list of all VMs in the vcenter

headers = {
    'vmware-api-session-id': '4814fdec7e9d177f54b2367dbc3e754a',
}

params = {
    'power_states': 'POWERED_ON',
}

vcenter_vm_list = requests.get('https://cwvc2.ccbc.ccbcmd.edu/api/vcenter/vm', params=params, headers=headers, verify=False)


vvl = vcenter_vm_list.text
inventory = json.loads(vvl)
inventory_df = pd.DataFrame(inventory)

#Isolate machine names and create list
machs = list(set(inventory_df['vm']))

#Get disk stats for a specific machine
# -2- Need to add routine so that it loops through the list of all machines

#contruct the desired commands and write them to a file
with open(r"C:\Users\rstuartii\OneDrive - The Community College of Baltimore County\Documents\reggie\VMware\api\requests", "a") as f:

    for x in machs:
        host = x
        cmd = ""+ x +"data = requests.get('https://cwvc2.ccbc.ccbcmd.edu/api/vcenter/vm/" + x + "/guest/local-filesystem', headers=headers, verify=False,)"
        print(cmd, file=f)
                       
#

disk_stats = requests.get(
    'https://cwvc2.ccbc.ccbcmd.edu/api/vcenter/vm/vm-108961/guest/local-filesystem',
    headers=headers,
    verify=False,
)

dst = disk_stats.text
disk_usage = json.loads(dst)
dud = pd.DataFrame(disk_usage)

#Remove troublesome characters

dud.columns = dud.columns.str.replace(':', '')
dud.columns = dud.columns.str.replace('\\', '')

# -1- DONE: Need to calculate percentage free and report

percent_free = dud['C'].iloc[1] / dud['C'].iloc[2]
pfree = percent_free
threed = round(pfree,3)  #gives us a decimal to 3 places that is still a number, not a string
printpercent = format(pfree, ".000%")   #gives us a string we print



#REPORT PHASE OF PROGRAM

#Present percent
print ("free space on XYZ drive C:\ is " + printpercent + " percent of capacity")


#Sort data in the order we desire.
