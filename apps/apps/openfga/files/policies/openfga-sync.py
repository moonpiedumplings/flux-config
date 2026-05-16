import json
from authentik.core.models import Group

system_groups = ["authentik Read-only", "authentik Admins"]

all_groups = [group.name for group in Group.objects.all()]

all_groups = list(set(all_groups) - set(system_groups))

user_groups = [group.name for group in request.user.all_groups()]

openfga_api_key = ""

auth_model = ""

store_id = ""

writes = {
    "writes": {
        "tuple_keys": [
            {
                "user": f"user:{request.user.username}",
                "relation": "member",
                "object": "group"
            }
        ]
    },
    "authorization_model_id": f"{auth_model}"
}

user_project_writes = {
    "writes": {
        "tuple_keys": [
            {
                "user": f"user:{request.user.username}",
                "relation": "operator",
                "object": f"project:{request.user.username}"
            }
        ]
    },
    "authorization_model_id": f"{auth_model}"
}

deletes = {
    "deletes": {
        "tuple_keys": [
            {
                "user": f"user:{request.user.username}",
                "relation": "member",
                "object": "group"
            }
        ]
    },
    "authorization_model_id": f"{auth_model}"
}

network_writes = {
    "writes": {
        "tuple_keys": [
            {
                "network": f"network:{request.user.username}-cloudnet",
                "relation": "project",
                "object": f"project:{request.user.username}"
            }
        ]
    },
    "authorization_model_id": f"{auth_model}"
}

vlab_writes = {
    "writes": {
        "tuple_keys": [
            {
                "network": f"network:{request.user.username}-vlab",
                "relation": "project",
                "object": f"project:{request.user.username}"
            }
        ]
    },
    "authorization_model_id": f"{auth_model}"
}


headers = {
    "Authorization": f"Bearer {openfga_api_key}",
    "content-type": "application/json"
}


for group in list(set(all_groups) - set(user_groups)):
  deletes["deletes"]["tuple_keys"][0]["object"] = f"group:{group}"
  requests.post(f"https://openfga.moonpiedumpl.ing/stores/{store_id}/write", data=json.dumps(deletes), headers=headers)


requests.post(f"https://openfga.moonpiedumpl.ing/stores/{store_id}/write", data=json.dumps(vlab_writes), headers=headers)

# TODO
# Add another request that auto gives groups access to projects by the same name

requests.post(f"https://openfga.moonpiedumpl.ing/stores/{store_id}/write", data=json.dumps(network_writes), headers=headers)

requests.post(f"https://openfga.moonpiedumpl.ing/stores/{store_id}/write", data=json.dumps(user_project_writes), headers=headers)

for group in user_groups:
    writes["writes"]["tuple_keys"][0]["object"] = f"group:{group}"
    requests.post(f"https://openfga.moonpiedumpl.ing/stores/{store_id}/write", data=json.dumps(writes), headers=headers)

return True