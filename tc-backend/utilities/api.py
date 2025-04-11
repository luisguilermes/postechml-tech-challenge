from flask import Flask, jsonify
import sys
import os
from flasgger import Swagger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from embrapa_scraper.scraping import Scraping

dados = Scraping()
app = Flask(__name__)
swagger = Swagger(app)  ## Testar: http://localhost:5000/apidocs/

@app.route("/api", methods=["GET"])
def Home():
    """
    GET - EXIBINDO DADOS DA API
    ---
    parameters:
      - name: N/A
        in: query
        type: JSON
        required: true
        description: dados embrapa
    responses:
      200:
        description: dados embrapa
        schema:
          type: object
          properties:
            resultado:
              type: JSON
              example: dados
    """
    return  {"dados":dados}
    
if __name__ == "__main__":
    app.run(debug=True)