import requests
import redis 
import ast
API_URL = "https://backboard.railway.app/graphql/v2"
TOKEN = "43687474-171f-4267-a327-a3293dd830e0"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

REDIS_HOST = "redis-11050.c212.ap-south-1-1.ec2.cloud.redislabs.com"
REDIS_PORT = 11050
REDIS_USERNAME = "default"
REDIS_PASSWORD = "acPb6A0sK3tfpbzwNyev94yDfsUPRWLr"
REDIS_DB = 0
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, username=REDIS_USERNAME, password=REDIS_PASSWORD, db=REDIS_DB)
did = ast.literal_eval(r.get("deploymentids").decode("utf-8"))
print(list(did), type(did))


if did:
    print("Fetched deployment ids from redis:", did)
    for d in did:
        query = f"""
        mutation
        {{
          deploymentRemove(id:"{d}")
        }}    """
        resp = requests.post(API_URL, headers=headers, json={"query": query})
        print(f"Removed deployment {d}: {resp.json()}")

print("All deployments removed.", did)
r.set("deploymentids", "")

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