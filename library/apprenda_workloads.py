#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from email.header import Header
import requests
import json

def authenticate(url, user, password, tenant):
    auth_url = "{0}/authentication/api/v1/sessions/developer".format(url)
    auth_data = {
        'username': user,
        'password': password,
        'tenant': tenant
    }
    resp = requests.post(auth_url, verify=False, json=auth_data)
    resp_json = resp.json()
    return resp_json['apprendaSessionToken']

def get_workloads(auth_token, apprenda_url, app_alias, version_alias, component_alias):
    apps_url = "{0}/soc/api/v1/applications/{1}/versions/{2}/components/{3}/workloads".format(apprenda_url, app_alias, version_alias, component_alias)
    resp = requests.get(apps_url, verify=False, headers=auth_token)
    return resp.json(), 0

def deploy_workload(auth_token, apprenda_url, app_alias, version_alias, component_alias, node_name):
    apps_url = "{0}/soc/api/v1/applications/{1}/versions/{2}/components/{3}/workloads".format(apprenda_url, app_alias, version_alias, component_alias)
    apps_data = {
        'nodeName': node_name,
    }
    resp = requests.post(apps_url, json=apps_data, verify=False, headers=auth_token)
    if resp.status_code != 204:
        return "Failed with status code: {0} with detail: {1}".format(resp.status_code, resp.text), 1
    return resp.status_code, 0

def delete_workload(auth_token, apprenda_url, app_alias, version_alias, component_alias, workload_id):
    apps_url = "{0}/soc/api/v1/applications/{1}/versions/{2}/components/{3}/workloads/{4}".format(apprenda_url, app_alias, version_alias, component_alias, workload_id)
    resp = requests.delete(apps_url, verify=False, headers=auth_token)
    if resp.status_code != 204:
        return resp.status_code, 1
    return resp.status_code, 0

def get_workload(auth_token, apprenda_url, app_alias, version_alias, component_alias, workload_id):
    apps_url = "{0}/soc/api/v1/applications/{1}/versions/{2}/components/{3}/workloads/{4}".format(apprenda_url, app_alias, version_alias, component_alias, workload_id)
    resp = requests.get(apps_url, verify=False, headers=auth_token)
    return resp.json(), 0

def get_all_workloads_by_node(auth_token, apprenda_url, node_name):
    apps_url = "{0}/soc/api/v1/nodes/workloads?nodename={1}".format(apprenda_url, node_name)
    resp = requests.get(apps_url, verify=False, headers=auth_token)
    return resp.json(), 0

def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(required=True, choices=['get_workloads', 'deploy_workload', 'delete_workload', 'get_workload', 'get_all_workloads_by_node']),
            apprenda_url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            tenant=dict(type='str', required=True),
            app_alias=dict(type='str', required=False),
            version_alias=dict(type='str', required=False),
            component_alias=dict(type='str', required=False),            
            node_name=dict(type='str', required=False),            
            workload_id=dict(type='str', required=False),            
        )
    )

    action = module.params['action']
    apprenda_url = module.params['apprenda_url']
    username = module.params['username']
    password = module.params['password']
    tenant = module.params['tenant']
    app_alias = module.params['app_alias']
    version_alias = module.params['version_alias']
    component_alias = module.params['component_alias']
    node_name = module.params['node_name']
    workload_id = module.params['workload_id']
    node_name = module.params['node_name']

    auth_token_string = authenticate(apprenda_url, username, password, tenant)
    auth_token = { "ApprendaSessionToken": str(Header(auth_token_string, 'utf-8')) }

    if action == "get_workloads":
        (out, rc) = get_workloads(auth_token, apprenda_url, app_alias, version_alias, component_alias)
    if action == "deploy_workload":
        (out, rc) = deploy_workload(auth_token, apprenda_url, app_alias, version_alias, component_alias, node_name)
    if action == "delete_workload":
        (out, rc) = delete_workload(auth_token, apprenda_url, app_alias, version_alias, component_alias, workload_id)
    if action == "get_workload":
        (out, rc) = get_workload(auth_token, apprenda_url, app_alias, version_alias, component_alias, workload_id)
    if action == "get_all_workloads_by_node":
        (out, rc) = get_all_workloads_by_node(auth_token, apprenda_url, node_name)
    if (rc != 0):
        module.fail_json(msg="failure", result=out)
    else:
        module.exit_json(msg="success", result=out)

if __name__ == '__main__':
    main()
