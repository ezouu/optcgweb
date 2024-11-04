from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import time

# Load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)  # Use the URI from the environment variable
db = client['my_database']  # Database name
collection = db['card_prices']  # Collection name

# Specify the path to the ChromeDriver
service = Service(executable_path='main/chromedriver')

# Set up Selenium with Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=service, options=options)

# List of URLs and set names
sets = [
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/romance-dawn", "set_name": "Romance Dawn"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/paramount-war", "set_name": "Paramount War"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/pillars-of-strength", "set_name": "Pillars of Strength"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/kingdoms-of-intrigue", "set_name": "Kingdoms of Intrigue"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/awakening-of-the-new-era", "set_name": "Awakening of the New Era"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/wings-of-the-captain", "set_name": "Wings of the Captain"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/500-years-in-the-future", "set_name": "500 Years in the Future"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/two-legends", "set_name": "Two Legends"}
]

# Define a retry function
def scrape_set(set_info, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            # Scraping logic
            url = set_info["url"]
            set_name = set_info["set_name"]
            print(f"Scraping data for set: {set_name}")

            # Navigate to the URL
            driver.get(url)

            # Wait until the table is present
            table = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div/section[2]/section/div[3]/div/div/div/div[2]/div[2]/div[1]/table"))
            )
            
            # Extract each row from the table
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            
            # Collect data in a list for MongoDB
            data = []
            for idx, row in enumerate(rows, start=1):
                try:
                    rarity = row.find_element(By.XPATH, "./td[6]").text
                    number = row.find_element(By.XPATH, "./td[7]").text
                    price = row.find_element(By.XPATH, "./td[8]").text
                    link_element = row.find_element(By.XPATH, "./td[2]/a")
                    card_link = link_element.get_attribute("href")

                    # Extract the unique card code from the URL
                    unique_code = card_link.split('/product/')[1].split('/')[0]
                    image_url = f"https://tcgplayer-cdn.tcgplayer.com/product/{unique_code}_in_200x200.jpg"

                    print(f"Set: {set_name}, Rarity: {rarity}, Number: {number}, Price: {price}, URL: {card_link}, Image URL: {image_url}")

                    # Add data to MongoDB with the new Image URL field
                    data.append({
                        "_id": f"{set_name}_{idx}",
                        "Set": set_name,
                        "Rarity": rarity,
                        "Number": number,
                        "Market Price": price,
                        "Product URL": card_link,
                        "Image URL": image_url
                    })
                except Exception as e:
                    print(f"Error extracting data from row {idx} in {set_name}: {e}")


            # Insert data into MongoDB (upserts by unique _id for each card)
            for card in data:
                collection.replace_one({"_id": card["_id"]}, card, upsert=True)

            print(f"Successfully uploaded {len(data)} cards for set: {set_name}")
            return  # Exit the function on success

        except (TimeoutException, WebDriverException) as e:
            print(f"Attempt {retries + 1} failed for set {set_name}: {e}")
            retries += 1
            time.sleep(5)  # Optional: wait before retrying

    print(f"Failed to scrape set {set_name} after {max_retries} attempts")

# Main execution loop
try:
    for set_info in sets:
        scrape_set(set_info)

finally:
    driver.quit()
    client.close()  # Close MongoDB connection when done
