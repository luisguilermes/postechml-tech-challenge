#importações
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

#Dados da Pagina de Produção
def Scraping() -> list:
    #Anos
    anos = list(range(1970, 2025)) 
    coleta = datetime.now().isoformat() + "Z"

    dados_formatados = []

    #for
    for ano in anos:
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        itens = soup.find_all(class_="tb_item")
        categorias_raw = [i.get_text(strip=True) for i in itens]

        categorias = [(categorias_raw[i], categorias_raw[i+1]) for i in range(0, len(categorias_raw), 2)]

        descricoes = soup.find_all(class_="tb_subitem")
        descricoes_raw = [d.get_text(strip=True) for d in descricoes]
        descricoes_pares = [(descricoes_raw[i], descricoes_raw[i+1]) for i in range(0, len(descricoes_raw), 2)]


        idx = 0
        for categoria, total in categorias:
            for _ in range(3):  
                if idx >= len(descricoes_pares):
                    break
                subcategoria, valor = descricoes_pares[idx]
                idx += 1
                if valor == "-" or not valor.strip():
                    continue
                try:
                    valor_limpo = int(valor.replace(".", ""))
                except:
                    continue
                dados_formatados.append({
                    "category": categoria,
                    "sub_category": subcategoria,
                    "amount": valor_limpo,
                    "year": ano,
                    "source": "Embrapa/Vitivinicultura",
                    "collected_at": coleta
                })

    dados = json.dumps(dados_formatados, indent=4, ensure_ascii=False)
    return dados_formatados

#print(dados)
#print(dados_formatados)
