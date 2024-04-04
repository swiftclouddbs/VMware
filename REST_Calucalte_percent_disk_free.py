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
    'vmware-api-session-id': 'a04dfa9dbddefe4cff9d39f034a316bb',
}
 
params = {
    'power_states': 'POWERED_ON',
}
 
vcenter_vm_list = requests.get('https://cwvc2.ccbc.ccbcmd.edu/api/vcenter/vm', params=params, headers=headers, verify=False)
 
vvl = vcenter_vm_list.text
inventory = json.loads(vvl)
inventory_df = pd.DataFrame(inventory)
#filter on CW machines
cwindows = inventory_df[inventory_df['name'].str.contains("CW")]
 
#Isolate machine names and create list
machs = list(set(cwindows['vm']))
 
#Get stats from each machine and write to a file.
 
with open(r"C:\Users\rstuartii\OneDrive - The Community College of Baltimore County\Documents\reggie\VMware\api\stats", "a") as f:
 
    for x in machs:
        cmd = requests.get('https://cwvc2.ccbc.ccbcmd.edu/api/vcenter/vm/' + x + '/guest/local-filesystem', headers=headers, verify=False,)
        cmd
        dst = cmd.text
        disk_usage = json.loads(dst)
        dud = pd.DataFrame(disk_usage)
        print(x, dud, file=f)
 
###Format and perform final calculations
##
##        dud.columns = dud.columns.str.replace(':', '')
##        dud.columns = dud.columns.str.replace('\\', '')
##        percent_free = dud['C'].iloc[1] / dud['C'].iloc[2]
##        pfree = percent_free
##        threed = round(pfree,3)  #gives us a decimal to 3 places that is still a number, not a string
##        printpercent = format(pfree, ".000%")   #gives us a string we print
##
###Print percent
##        print ("free space on " + x + "drive C:\ is " + printpercent + " percent of capacity")
##
##
###Sort data in the order we desire.




