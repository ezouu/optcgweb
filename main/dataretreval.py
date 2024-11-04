from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
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
        {"id": 1, "name": "Romance Dawn", "image": "Romance Dawn.jpg"},
        {"id": 2, "name": "Paramount War", "image": "Paramount War.jpg"},
        {"id": 3, "name": "Pillars of Strength", "image": "Pillars of Strength.jpg"},
        {"id": 4, "name": "Kingdoms of Intrigue", "image": "Kingdoms of Intrigue.jpg"},
        {"id": 5, "name": "Awakening of the New Era", "image": "Awakening of the New Era.jpg"},
        {"id": 6, "name": "Wings of the Captain", "image": "Wings of the Captain.jpg"},
        {"id": 7, "name": "500 Years in the Future", "image": "500 Years in the Future.jpg"},
        {"id": 8, "name": "Two Legends", "image": "Two Legends.jpg"}
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
