from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
url = 'https://www.tcgplayer.com/product/558160?Language=English'
driver.get(url)

try:
    # Locate the price element using the updated XPath
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/section[2]/section/div[2]/div[2]/section[2]/section[1]/div/section[2]/span"))
    )
    price = price_element.text
    print(f"Price: {price}")
    
    # Locate the tag element using the updated XPath
    tag_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/section[2]/section/div[2]/div[2]/section[2]/section[3]/div/div/div[1]/div/ul/li[2]/div/span"))
    )
    tag_number = tag_element.text
    print(f"Tag Number: {tag_number}")

except TimeoutException:
    print("Could not find the price or tag number on the page.")
finally:
    driver.quit()
