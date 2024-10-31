from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tabulate import tabulate
import os
from dotenv import load_dotenv
from pymongo import MongoClient

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

# The URL you provided
url = 'https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/romance-dawn'
driver.get(url)

try:
    # Wait until the table is present
    table = WebDriverWait(driver, 10).until(
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
            print(f"Rarity: {rarity}, Number: {number}, Price: {price}")  # Debugging print
            data.append({"_id": idx, "Rarity": rarity, "Number": number, "Price": price})  # For MongoDB
        except Exception as e:
            print(f"Error extracting data from row {idx}: {e}")

    # Insert data into MongoDB (overwrites if document with same _id exists)
    for card in data:
        collection.replace_one({"_id": card["_id"]}, card, upsert=True)
    
    # Print the table using tabulate
    headers = ["#", "Rarity", "Number", "Price"]
    table_data = [[idx, item["Rarity"], item["Number"], item["Price"]] for idx, item in enumerate(data, start=1)]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

except TimeoutException:
    print("Could not find the table on the page.")
finally:
    driver.quit()
    client.close()  # Close MongoDB connection when done
