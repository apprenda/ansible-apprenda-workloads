Apprenda Workloads
=========

This role enables management of Apprenda Application Workloads through the System Operations Center.

Requirements
------------

* Apprenda Cloud Platform v7.1 or higher
* Python requests library (`pip install requests`)
* Python apprendaapipythonclient Library (`pip install apprendaapipythonclient`)

Role Variables
--------------

`apprenda_url` - FQDN of your ACP instance (i.e, `https://apps.apprenda.com`) **Required**

`username` - Platform user to execute role actions under. **Required**

`password` - Password of the platform user. **Required**

`tenant` - Tenant Alias of the platform user. **Required**

`action` - The action to perform. This can be one of the following. Required parameters for each action are below the action. **Required**
- `get_workloads`: Retrieves the workloads for an application component.
  - `app_alias`: The application alias.
  - `version_alias`: The version alias.
  - `component_alias`: The component alias.
- `get_workload`: Retrieves detailed information about a specific workload.
  - `app_alias`: The application alias.
  - `version_alias`: The version alias.
  - `component_alias`: The component alias.
  - `workload_id`: The workload identifier.
- `deploy_workload`: Deploy a new workload for an existing application component to a new node.
  - `app_alias`: The application alias.
  - `version_alias`: The version alias.
  - `component_alias`: The component alias.
  - `node_name`: The node name to deploy to.
- `delete_workload`: Destroy a deployed workload.
  - `app_alias`: The application alias.
  - `version_alias`: The version alias.
  - `component_alias`: The component alias.
  - `workload_id`: The workload identifier.
- `get_all_workloads_by_node`: Retrieves all workloads running on a specified node.
  - `node_name`: The node name to retrieve running workloads on.

Dependencies
------------


Example Playbook
----------------

This demonstrates how to get workloads, start new workloads, and remove existing workloads.

```
---
- hosts: localhost
  vars:
    apprenda_url: "https://apps.apprenda.bxcr"
    username: "bxcr@apprenda.com"
    password: "password"
    tenant: "developer"
roles:
  - role: "apprenda_workloads"
    action: "get_all_workloads_by_node"
    node_name: "bxcr01"

  - role: "apprenda_workloads"
    action: "get_workloads"
    app_alias: "account"
    version_alias: "v7.1.0"
    component_alias: "ui-root"

  - role: "apprenda_workloads"
    action: "deploy_workload"
    app_alias: "account"
    version_alias: "v7.1.0"
    component_alias: "ui-root"
    node_name: "bxcr02"

  - role: "apprenda_workloads"
    action: "get_workload"
    app_alias: "account"
    version_alias: "v7.1.0"
    component_alias: "ui-root"
    workload_id: "36"

  - role: "apprenda_workloads"
    action: "delete_workload"
    app_alias: "account"
    version_alias: "v7.1.0"
    component_alias: "ui-root"
    workload_id: "36"

```

License
-------

MIT

Author Information
------------------

Please see http://www.apprenda.com for more information about the Apprenda Cloud Platform.