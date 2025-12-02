import requests, os
from time import sleep
import redis 

REDIS_HOST = "redis-11050.c212.ap-south-1-1.ec2.cloud.redislabs.com"
REDIS_PORT = 11050
REDIS_USERNAME = "default"
REDIS_PASSWORD = "acPb6A0sK3tfpbzwNyev94yDfsUPRWLr"
REDIS_DB = 0
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, username=REDIS_USERNAME, password=REDIS_PASSWORD, db=REDIS_DB)
API_URL = "https://backboard.railway.app/graphql/v2"
TOKEN = "43687474-171f-4267-a327-a3293dd830e0"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
environmentId = "f45f96ae-51dc-486d-8b82-088290cfb980"
services = [
    {"serviceId": "0dc16b12-99be-448f-bdbd-1f16c0360509", "environmentId": environmentId},
    {"serviceId": "73d9ef1c-2720-466f-962a-a1bce58de630", "environmentId": environmentId},
    {"serviceId": "f12a7630-dc48-4c78-8597-656cb85714d1", "environmentId": environmentId},
    {"serviceId": "ee2718c0-b26f-49b0-9904-4ee4bceef3c4", "environmentId": environmentId}
]


def deploy_service(svc):
    query = f"""
        mutation
        {{
        serviceInstanceDeployV2(environmentId: "{svc['environmentId']}", serviceId:"{svc['serviceId']}")
        }}    """
    resp = requests.post(API_URL, headers=headers, json={"query": query})
    print(f"Triggered deployment for {svc['serviceId']}: {resp.json()}")
    return  resp.json()["data"]["serviceInstanceDeployV2"]

# Run non-depending deployments first


deploymentids = []
deploymentids.append(deploy_service(services[0]))  # Example call for first service
deploymentids.append(deploy_service(services[1]))  # Example call for second service

# Wait for some time to let the non-depending deployments stabilize
sleep(90)
deploymentids.append(deploy_service(services[2]))  # Example call for third service   
deploymentids.append(deploy_service(services[3]))  # Example call for fourth service
print("All deployments triggered.", deploymentids)
r.set("deploymentids", str(deploymentids))
"""
mutation
{
  serviceInstanceDeployV2(environmentId: "f45f96ae-51dc-486d-8b82-088290cfb980", serviceId:"0dc16b12-99be-448f-bdbd-1f16c0360509")
}

mutation
{
  deploymentRemove(id:"a96a7b1a-34c1-432a-85dc-1e263e5784e4")
}

"""