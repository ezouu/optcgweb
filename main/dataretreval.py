from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB setup
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client['my_database']
collection = db['card_prices']

@app.route('/cards', methods=['GET'])
def get_all_cards():
    rarity = request.args.get('rarity')  # Optional filter for rarity
    query = {"Rarity": rarity} if rarity else {}
    cards = list(collection.find(query, {'_id': 0}))
    return jsonify(cards)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
