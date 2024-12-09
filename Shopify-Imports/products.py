import requests, csv, os, model
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
url_graphql = os.environ.get("url_graphql")
headers = {
"X-Shopify-Access-Token":os.environ.get("X-Shopify-Access-Token"),
"Content-Type":"application/json"
}

def get_all_Products():
    products = []  # Store all retrieved products
    last_cursor = None  # Start with no cursor for the first page
    
    query = """
    query ($lastCursor: String) {
      products(first: 10, after: $lastCursor) {
        edges {
          node {
            id
            status
            variants(first:10){
            edges{
                node{
                    price
                    sku
                    inventoryQuantity
                }
            }
        }
            media (first:10){
              nodes {
                id
              }
            }
          }
          cursor
        }
        pageInfo {
          endCursor
        }
      }
    }
    """
    
    while True:
        # Prepare variables
        variables = {"lastCursor": last_cursor}
        
        # Send the GraphQL request
        response = requests.post(url=url_graphql, json={"query": query, "variables": variables}, headers=headers)
        
        # Check for response success
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        
        data = response.json()
        print(data)
        
        # Extract product data
        edges = data["data"]["products"]["edges"]
        for edge in edges:
          medias = edge.get("node").get("media").get("nodes")
          midia = [media.get("id") for media in medias]
          
          newDict={
              "id":edge.get("node").get("id"),
              "SKU":edge.get("node").get("variants").get("edges")[0].get("node").get("sku").strip().replace(".","").replace(" ",""),
              "price":edge.get("node").get("variants").get("edges")[0].get("node").get("price"),
              "inventoryQuantity":edge.get("node").get("variants").get("edges")[0].get("node").get("inventoryQuantity"),
              "Media": midia,
              "len":len(midia),
              "status":edge.get("node").get("status"),
          }
          products.append(newDict)
        page_info = data.get("data", {}).get("products", {}).get("pageInfo", {})
          
        
        # Check if there are more pages
        last_cursor = page_info.get("endCursor")
        if not last_cursor:
            break  # Exit the loop when there are no more pages
    
    # Define the CSV file path
    csv_file_path = "/home/devops2/projects/fastprojects/gimena_import/products.csv"
    
    # Define the CSV field names
    fieldnames = ["id", "SKU","price", "Media","len","status", "inventoryQuantity"]
    
    # Write the products to a CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      
      # Write the header
      writer.writeheader()
      
      # Write the product data
      for product in products:
        writer.writerow(product)
    
    print(f"Products have been written to {csv_file_path}")
    
def update_ProductWithImage(filepath,outputfilepath):
    with open(filepath,"r",encoding="utf-8") as productWithImagesFile:
        df = pd.read_csv(productWithImagesFile,delimiter=";")
        
        if "status" not in df.columns:
            df["status"] = ""        
    for indice,linha in df.iterrows():
        productID = linha['id']
        sku = linha['SKU']
        print(f"Acessando  o produto: {productID} | SKU: {sku} - Indice: {indice}")
        imagens = linha['New images'].split(",")
        for imagem in imagens:
            print(f"Carregando imagem: {imagem}")
            query,variables = model.put_productsWithImage(productID=productID,mediaID=imagem.replace("[","").replace("]","").strip(),alt=sku)
            payload = {
                    "query":query,
                    "variables":variables
                }
            response = requests.post(url=url_graphql,headers=headers,json=payload)
            print(response.json())
        
        df.at[indice,"status"] = "Done"
        
    df.to_csv(outputfilepath,sep=";",index=False)