from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)  # Use the URI from the environment variable
db = client['my_database']  # Database name
collection = db['card_prices']  # Collection name

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    # List of sets (boxes)
    sets = [
        {"name": "Romance Dawn", "id": 1},
        {"name": "Paramount War", "id": 2},
        {"name": "Pillars of Strength", "id": 3},
        {"name": "Kingdoms of Intrigue", "id": 4},
        {"name": "Awakening of the New Era", "id": 5},
        {"name": "Wings of the Captain", "id": 6},
        {"name": "500 Years in the Future", "id": 7},
        {"name": "Two Legends", "id": 8}
    ]
    return render_template('index.html', sets=sets)

# Route for viewing the contents of a specific box
@app.route('/box/<set_name>')
def view_box(set_name):
    # Fetch all cards in the selected set
    cards = list(collection.find({"Set": set_name}))
    return render_template('box.html', set_name=set_name, cards=cards)

if __name__ == '__main__':
    app.run(debug=True)
