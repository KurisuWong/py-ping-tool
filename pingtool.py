import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime # For using time date as filename
import yaml
import time

# Helper Function
def getCurrentTime():
    return datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def printConfig():
    # Read config file
    print('==========')
    print('| CONFIG |')
    print('==========')
    print('IPLIST_PATH: {IPLIST_PATH}'.format(IPLIST_PATH=config['IPLIST_PATH']))
    print('TIME_DELAY: {TIME_DELAY}'.format(TIME_DELAY=config['TIME_DELAY']))
    print('TIME_DELAY_LIST: {TIME_DELAY_LIST}'.format(TIME_DELAY_LIST=config['TIME_DELAY_LIST']))
    print('\n')

# Main
with open('config.yml') as stream:
    config = yaml.safe_load(stream)

printConfig()

# Opening file
ipList = open(config['IPLIST_PATH'], 'r')

while True:
    # Result file
    logFilename = getCurrentTime() + '_result.log'
    result_file = open(logFilename, 'w')

    # loop every ip in list
    for ip in ipList:
        if ping(ip.strip()):
            result_file.write('{date} \t Host {ip} \t UP \n'.format(date=getCurrentTime(),ip=ip.strip()))
        else:
            result_file.write('{date} \t Host {ip} \t DOWN \n'.format(date=getCurrentTime(),ip=ip.strip()))

        # delay before next ping
        time.sleep(config['TIME_DELAY'])
    
    # close result file
    result_file.close()

    # sleep before next round
    if config['TIME_DELAY_LIST'] < 0:
        print('[INFO] Config file set to ping the whole list once only, program existing.')
        break
    else:
        print('[INFO] Resume after {TIME_DELAY_LIST}s'.format(TIME_DELAY_LIST=config['TIME_DELAY_LIST']))
        time.sleep(config['TIME_DELAY_LIST'])

# programe end, close ipList
ipList.close()

print("End")