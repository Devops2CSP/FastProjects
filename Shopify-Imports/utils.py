import json,csv
import pandas as pd

def json_to_csv(json_file, csv_file):
        # Load JSON data from the file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract headers from the keys of the first dictionary
    headers = data[0].keys()
    
    # Write to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def concatenate_images(filepath):
    """Concatena as linhas referentes a mesma peça na planilha de imagens e transforma em lista as URLS
    """
    # Carregar os dados do Excel
    df = pd.read_csv(filepath,delimiter=";")

    # Agrupar por 'codpart' e consolidar as URLs em uma lista formatada
    df_consolidado = df.groupby('codpart')['url'].apply(lambda x: f"{' '.join(x)}").reset_index()

    # Salvar o resultado em um novo arquivo Excel
    df_consolidado.to_csv('consolidado.csv', index=False)
    
