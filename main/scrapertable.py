import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
import os
from dotenv import load_dotenv

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
    #{"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/romance-dawn", "set_name": "Romance Dawn"},
    #{"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/paramount-war", "set_name": "Paramount War"},
    #{"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/pillars-of-strength", "set_name": "Pillars of Strength"},
    {"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/kingdoms-of-intrigue", "set_name": "Kingdoms of Intrigue"},
    #{"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/awakening-of-the-new-era", "set_name": "Awakening of the New Era"},
    #{"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/wings-of-the-captain", "set_name": "Wings of the Captain"},
    #{"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/500-years-in-the-future", "set_name": "500 Years in the Future"},
    #{"url": "https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/two-legends", "set_name": "Two Legends"}
]

try:
    # Loop through each set
    for set_info in sets:
        url = set_info["url"]
        set_name = set_info["set_name"]
        print(f"Scraping data for set: {set_name}")

        # Navigate to the URL
        driver.get(url)

        try:
            # Wait until the table is present
            table = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/section[2]/section/div[3]/div/div/div/div[2]/div[2]/div[1]/table"))
            )
            
            # Extract each row from the table
            rows = table.find_elements(By.XPATH, "./tbody/tr")
            
            # Collect data in a list for tabulate and MongoDB
            data = []
            for idx, row in enumerate(rows, start=1):
                try:
                    rarity = row.find_element(By.XPATH, "./td[6]").text
                    number = row.find_element(By.XPATH, "./td[7]").text
                    price = row.find_element(By.XPATH, "./td[8]").text
                    print(f"Set: {set_name}, Rarity: {rarity}, Number: {number}, Price: {price}")  # Debugging print
                    
                    # Prepare data for MongoDB
                    card_data = {
                        "Set": set_name,
                        "Rarity": rarity,
                        "Number": number,
                        "Price": price
                    }
                    
                    # Upsert: Find by set name and number, update or insert if it doesn't exist
                    collection.update_one(
                        {"Set": set_name, "Number": number},
                        {"$set": card_data},
                        upsert=True
                    )
                    
                except Exception as e:
                    print(f"Error extracting data from row {idx} in {set_name}: {e}")

            # Wait for a specific status element to appear as a confirmation before proceeding
            status_confirmed = False
            try:
                # Example: Wait for a footer element to confirm readiness for the next link
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "footer"))
                )
                status_confirmed = True
                print(f"Status confirmed for {set_name}. Moving to the next set.")
            except TimeoutException:
                print(f"Status not confirmed for {set_name}. Proceeding with caution.")
            
        except TimeoutException:
            print(f"Could not find the table on the page for set: {set_name}")
        except Exception as e:
            print(f"An error occurred for set {set_name}: {e}")

finally:
    driver.quit()
    client.close()  # Close MongoDB connection when done
