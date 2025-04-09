from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/home', methods=['GET'])
def Home():
    """
    METODO GET - CONSUMO DE API
    ---
    parameters:
      - name: A definir...
        in: query
        type: string
        required: true
        description: descicao
    responses:
      200:
        description: A definir...
        schema:
          type: object
          properties:
            resultado:
              type: string
              example: x
    """
    teste = "Hello Fiap"
    return jsonify({'resultado': teste})

@app.route("/send", methods=["POST"])
def Sender():
    """
    METODO POST - REQUISIÇÕES PARA API
    ---
    parameters:
      - name: A definir...
        in: query
        type: string
        required: true
        description: descicao
    responses:
      200:
        description: A definir...
        schema:
          type: object
          properties:
            resultado:
              type: string
              example: x
    """
    pass

@app.route("/update", methods=["PUT"])
def Update():
    """
    METODO PUT - ATUALIZAR DADOS NA API
    ---
    parameters:
      - name: A definir...
        in: query
        type: string
        required: true
        description: descicao
    responses:
      200:
        description: A definir...
        schema:
          type: object
          properties:
            resultado:
              type: string
              example: x
    """
    pass

@app.route("/delete", methods=["DELETE"])
def Delete():
    """
    METODO DELETE - DELETARINFORMAÇÕES NA API
    ---
    parameters:
      - name: A definir...
        in: query
        type: string
        required: true
        description: descicao
    responses:
      200:
        description: A definir...
        schema:
          type: object
          properties:
            resultado:
              type: string
              example: x
    """
    pass

if __name__ == '__main__':
    app.run(debug=True)
