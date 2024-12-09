def InventoryItems(check:bool,lastcursor:str=None):
    if check:
        query_InventoryItems_first = """
        query inventoryItems {
            inventoryItems(first: 50) {
                nodes {
                    id
                    sku
                    
                }
                pageInfo{
                    hasNextPage
                    endCursor
                }
            }
        }
"""     
        return query_InventoryItems_first
    query_InventoryItems_last = f"""
            query inventoryItems {{
        inventoryItems(first: 10,after:"{lastcursor}") {{
            nodes {{
                id
                sku
            }}
            pageInfo{{
                hasNextPage
            }}
        }}
    }}
"""   
    return query_InventoryItems_last

def get_Quantity(id_item:str):
    query_Stock_Quantity = f"""
    query inventoryItem {{
    inventoryItem(id:"{id_item}") {{
        id
        sku
        inventoryLevels(first: 1) {{
            edges {{
                node {{
                    location{{
                        id
                    }}
                    quantities(names: ["available", "committed", "incoming", "on_hand", "reserved"]) {{
                        name
                        quantity
                    }}
                }}
            }}
        }}
    }}
}}
"""
    return query_Stock_Quantity

def put_Change_Quantities(inventory_item_id:str,location_id:str,quantity:int):
    query_Change_Quantities = """
    mutation InventorySet($input: InventorySetQuantitiesInput!) {
    inventorySetQuantities(input: $input) {
        inventoryAdjustmentGroup {
            createdAt
            reason
            changes {
                name
                delta
            }
        }
        userErrors {
            field
            message
        }
    }
}

"""
    variables =  {
    "input": {
        "name": "available",
        "reason": "correction",
        "ignoreCompareQuantity": True,
        "quantities": [
            {
                "inventoryItemId": f"{inventory_item_id}",
                "locationId": f"{location_id}",
                "quantity": quantity
            }
        ]
    }
}

    return  query_Change_Quantities, variables

def create_Product(title,vendor,description):
    query = """
mutation productCreate($input: ProductInput!) {
    productCreate(input: $input) {
        product {
            id
            variants(first:1){
                edges{
                    node{
                        inventoryItem{
                            id
                        }
                    }
                }
            }
        }
    }
}


"""
    variable = {
    "input": {
        "title": title,
        "vendor": vendor,
        "descriptionHtml":f"{description} <p><STRONG>Fabricante: </STRONG>{vendor}</p>"
    }
}
    return query,variable

def create_ProductWithImage(title,vendor,description):
    query = """
mutation CreateProductWithNewMedia($input: ProductInput!, $media: [CreateMediaInput!]) {
    productCreate(input: $input, media:$media) {
        product {
            id
            media(first:10){
                nodes{
                    mediaContentType
                }
            }
            variants(first:1){
                edges{
                    node{
                        inventoryItem{
                            id
                        }
                    }
                }
            }
        }
    }
}


"""
    variable = {
    "input": {
        "title": title,
        "vendor": vendor,
        "descriptionHtml":f"{description} <p><STRONG>Fabricante: </STRONG>{vendor}</p>"
    },
    "media":[
        {
            "originalSource":"https://www.autopecaspiloto.com.br/cdn/shop/files/fc5d2340f7815c35f843296d8dc83492_f90ecfa0-de6a-4d9d-a467-2888367e7873_700x.png",
            "mediaContentType":"IMAGE"
        }
    ]}

    return query,variable

def put_create_sku(id,sku):
    query = """
    mutation inventoryItemUpdate($id: ID!, $input: InventoryItemInput!) {
  inventoryItemUpdate(id: $id, input: $input) {
    inventoryItem {
      id
    }
  }
}
"""
    variables = {
    "id":id,
    "input":{
        "sku":sku,
        "tracked":True
    }
}
    return query,variables

def create_file(path,codigo):
    
    query = """ mutation fileCreate($files: [FileCreateInput!]!) {
    fileCreate(files: $files) {
        files {
        id
        fileStatus
        alt
        createdAt
        }
    }
    } """
    variablesList = []
    for item in path:
        variablesList.append({ 
                                  "alt": codigo,
                                  "contentType": "IMAGE",
                                  "originalSource": item 
                              })
    
    variables = {"files":variablesList}
    return query, variables

def get_products():
    query = """query ($lastCursor: String!) {
  products(first: 10, after:$lastCursor ) {
    edges {
      node {
        id
        title
        handle
        media{
            nodes{
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
    return query
    
def get_products_variants():
    query = """query {
  productVariants(first: 10) {
    edges {
      node {
        id
        sku
        price
        inventoryQuantity
        product{
            id
            title
        }
      }
    }
  }
}"""
    return query

def put_productsWithImage(productID,mediaID,alt):
    
    query = """mutation productCreateMedia($media: [CreateMediaInput!]!, $productId: ID!) {
  productCreateMedia(media: $media, productId: $productId) {
    product{
        id
    }
    media {
      id
      alt
      status
      ... on MediaImage {
        image {
          url
        }
      }
    }
    mediaUserErrors {
      field
      message
    }
  }
}
"""
    variables = {
        "media":{
            "alt":alt,
            "mediaContentType":"IMAGE",
            "originalSource":mediaID
        },
        "productId":productID
}
    return query, variables

def get_image_links(idImage):
    query = f"""
    query {{
      node(id: "{idImage}") {{
        id
        ... on MediaImage {{
          image {{
            url
          }}
        }}
      }}
    }}
    """

    return query