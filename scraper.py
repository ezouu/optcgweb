from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Specify the path to the ChromeDriver
service = Service(executable_path='/home/eqzou/eqzou/optcgwebsite/main/chromedriver')


# Set up Selenium with Chrome
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
    # Wait for the price element to load
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'spotlight_price'))
    )
    price = price_element.text
    print(f"Price: {price}")
    
    # Locate the tag number
    tag_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'OP08-118')]"))
    )
    tag_number = tag_element.text
    print(f"Tag Number: {tag_number}")

except TimeoutException:
    print("Could not find the price or tag number on the page.")
finally:
    driver.quit()
