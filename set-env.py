import boto3
import requests
import subprocess
import re
import os


def getInstanceId():
    r = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    return r.text

def getRegion():
    r = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document')
    return r.json()


def getTags(instanceId, region):
    client = boto3.client('ec2',region_name=region)
    response = client.describe_tags(
        DryRun=False,
        Filters=[
            {
                'Name': 'resource-id',
                'Values': [instanceId]
            },
        ]
    )
    return response['Tags']

def getEnv(tags):
    env = None
    for tag in tags:
        print(tag)
        print(" ")
        if tag['Key'] == 'Environment':
            print(tag)
            env = tag['Value']
    return env

def findString(env):
    enviroments = open('/etc/environment').read()
    if 'export NODE_ENV' in enviroments:
        new_env_file = re.sub('export\ NODE_ENV.*?\n', 'export NODE_ENV='+env+'\n', enviroments)
        out_file = open("/etc/environment", "w")
        out_file.write(new_env_file)
        out_file.close()
    else:
        with open("/etc/environment", "a") as myfile:
            myfile.write('\n'+'export NODE_ENV='+env+'\n')

instanceId = getInstanceId()
region = getRegion()['region']
tags = getTags(instanceId, region)
findString(getEnv(tags))