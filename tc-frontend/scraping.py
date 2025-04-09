#Importações
from bs4 import BeautifulSoup
import requests

#Configs
link = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_02"
response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')

#Obtendo dados do Site
subtotal = soup.find_all(class_="tb_item")
descricao = soup.find_all(class_="tb_subitem")

### Subtotal ###
#Lista Subtotal
lista_sub = []
for i in subtotal:
    abc = i.get_text(strip=True) # + "\n"
    lista_sub.append(abc)

#Função para obter Textos do Subtotal
def getTextSubtotal():  
    text_sub = []
    for i in range(0,len(lista_sub),2):
        text_sub.append(lista_sub[i]) 
    return text_sub

#Função para obter Valores do Subtotal
def getValorSubtotal():
    valores_sub = []
    for i in range(1,len(lista_sub),2):
        valores_sub.append(lista_sub[i])
    return valores_sub

### Descrição ###
#Lista descrição
lista_descr = []
for i in descricao:
    abc = i.get_text(strip=True)
    lista_descr.append(abc)

#Função para obter Textos da Descrição
def getTextDescr():
    text_descr = []
    for i in range(0, len(lista_descr),2):
        text_descr.append(lista_descr[i])
    return text_descr

#Função para obter Valores do Subtotal
def getValorDescr():
    valor_descr = []
    for i in range(1, len(lista_descr),2):
        valor_descr.append(lista_descr[i])
    return valor_descr




