from flask import Flask, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from embrapa_scraper.scraping import Scraping

dados = Scraping()

app = Flask(__name__)

@app.route("/api")
def Home():
    return {"dados":dados}
    
if __name__ == "__main__":
    app.run(debug=True)