# 🍇 Plataforma SaaS - Embrapa Vitivinicultura API

Projeto desenvolvido como parte do **Tech Challenge** do curso de _Machine Learning Engineering_ da **Pos Tech**, com o objetivo de transformar dados públicos da vitivinicultura brasileira em um serviço SaaS acessível, integrando scraping, API RESTful e modelos de machine learning.

---

## 🧠 Visão Geral

A vitivinicultura é uma atividade econômica relevante em várias regiões do Brasil. A Embrapa disponibiliza dados valiosos sobre produção, comercialização, importação e exportação de uvas e vinhos — porém, apenas em tabelas HTML estáticas.

Este projeto resolve esse problema ao:

- Automatizar a extração e padronização desses dados;
- Disponibilizar as informações via API RESTful;
- Fornecer previsões com modelos de **Machine Learning** baseados nos dados históricos;
- Oferecer uma **interface web interativa** e pronta para comercialização como um produto SaaS.

---

## 📦 Estrutura do Projeto (Monorepo)

Este repositório contém duas aplicações principais:

- [`tc-backend`](./tc-backend): Aplicação Flask em Python responsável por:

  - Scraping dos dados do site da Embrapa;
  - Exposição de dados via API RESTful;
  - Geração de previsões com ML.

- [`tc-frontend`](./tc-frontend): Interface web em React para visualização e consulta dos dados e previsões (em desenvolvimento).

---

## 🚀 Funcionalidades

### Backend (`tc-backend`)

- 🔍 Coleta automatizada de dados de:
  - Produção de uvas
  - Processamento
  - Comercialização
  - Importação e Exportação
- 🔧 API RESTful para acesso estruturado aos dados
- 🔮 Geração de previsões usando modelos de ML
- 🧠 Armazenamento de previsões e dados históricos no banco
- 🔐 (Opcional) Autenticação com JWT
- 📄 Documentação interativa via Swagger/OpenAPI

### Frontend (`tc-frontend`)

- 📊 Visualização de dados históricos e previsões
- 🕹️ Interação com filtros e categorias (região, tipo de uva, ano, etc.)
- 📈 Gráficos comparativos com séries temporais

---

## 🧠 Produtos derivados com ML

Os modelos de Machine Learning utilizam os dados históricos da plataforma como **features** para criar produtos derivados. Exemplos:

- 📈 Previsão de produção para próximos anos
  - Valor para o cliente: Ajudar produtores e cooperativas a planejar melhor sua produção
- 📊 Análise de mercado por tipo de produto
  - Valor para o cliente: Ajudar vinícolas a entender padrões de consumo e ajustar o portfólio
- ⚠️ Detecção de anomalias em séries históricas
  - Valor para o cliente: Identificar problemas ou oportunidades atípicas em regiões específicas
- 📍 Recomendação de países para exportação
  - Valor para o cliente: Indicar os países com maior potencial de compra baseado em tendências históricas

Esses produtos podem ser comercializados como dashboards, APIs, relatórios automatizados ou serviços de assinatura.

---

## 🔗 Fonte de Dados

Todos os dados são extraídos automaticamente do portal oficial da Embrapa:
🔗 [http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01)

---

## 🧭 Arquitetura (Modelo C4 - Contexto)

O sistema é composto por:

- Scraper e previsão embarcados no mesmo backend (`tc-backend`)
- Interface web (`tc-frontend`) que consome os dados e previsões da API
- Banco de dados que armazena dados históricos e resultados de previsão

![Arquitetura - Modelo C4](./docs/architecture/c4/rendered/C4_Context.png)

---

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: React (JavaScript)
- **Scraping**: BeautifulSoup, Requests
- **Machine Learning**: Scikit-learn, Prophet, pandas
- **Banco de Dados**: PostgreSQL
- **Documentação**: Swagger (Flasgger ou FastAPI Docs)

---

## 📁 Instalação e Execução

### Requisitos

- Python 3.10+
- Node.js (para frontend)
- PostgreSQL

### Backend

```bash
cd tc-backend
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```
