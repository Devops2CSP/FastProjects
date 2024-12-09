import json,requests,os, model
from dotenv import load_dotenv

load_dotenv()
url_graphql = os.environ.get("url_graphql")
headers = {
"X-Shopify-Access-Token":os.environ.get("X-Shopify-Access-Token"),
"Content-Type":"application/json"
}


def create_Images(filepath):
    results = []   
    with open(filepath, "r") as imagesFP:
        images:dict = json.load(imagesFP)

    for key, value in images.items():
        alt= key
        origin = value
        query,variables = model.create_file(path=origin,codigo=alt)
        payload:dict = {"query":query,"variables":variables}
        response = requests.post(url=url_graphql,headers=headers,json=payload).json()
        items = response["data"]["fileCreate"]["files"]
        for item in items:
            result = {item.get("alt"):item.get("id")}
            results.append(result)       
    doc = open("resultsFileImport.json","w")
    json.dump(results,doc)

def getImageLink(value):
    query = model.get_image_links(value)
    payload = {"query":query}
    response = requests.post(url=url_graphql,headers=headers,json=payload).json()
    
    url = response["data"]["node"]["image"]["url"]
    return url