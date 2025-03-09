import time
from car import Car
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def initialize_chrome_webdriver():
    print("Initializing Chrome WebDriver...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

driver = initialize_chrome_webdriver()
driver.get("https://www.tesla.com/inventory/used/m3?PAINT=BLACK,GREY,RED&INTERIOR=PREMIUM_BLACK&VehicleHistory=CLEAN&Year=2022,2023,2024&arrangeby=distance&zip=33178&range=0")

# Force the script to wait for 15 seconds and let the inventory load
time.sleep(15)

wait = WebDriverWait(driver, 15)
results_container = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, "div.results-container.results-container--grid.results-container--has-results")
))

results = results_container.find_elements(By.CSS_SELECTOR, "article.result.card")
cars = []

# Iterate through the results and create Model3 objects from the HTML content
for result in results:
    try:
        button = result.find_element(By.TAG_NAME, "button")
        article = button.find_element(By.TAG_NAME, "article")
        card_info = article.find_element(By.CLASS_NAME, "card-info")
        section = card_info.find_element(By.TAG_NAME, "section")

        # Extract car information from the section tag
        type = section.find_element(By.CLASS_NAME, "tds-text--h4").text
        price = section.find_element(By.XPATH, ".//div/span/span").text
        description = section.find_element(By.CLASS_NAME, "tds-text--contrast-low").text
        range = section.find_elements(By.CLASS_NAME, "tds-text--contrast-low")[1].text

        car = Car(type=type, price=price, description=description, range=range)
        cars.append(car)
    except Exception as e:
        print(f"Skipping false result...")

driver.quit()

potential_prospects = []

# Iterate through the cars and identify potential prospects
for i, car in enumerate(cars):
    print(f"Result {i + 1}:\n{car}\n")

    try:    
        parsed_price = int(car.price.replace("$", "").replace(",", ""))
    except Exception as e:
        print(f"Could not parse the price of the car.\n")

    if parsed_price <= 26000:
        print("Found a potential prospect")
        potential_prospects.append(car)

if potential_prospects:
    for i, car in enumerate(potential_prospects):
        print(f"Potential prospect {i + 1}:\n{car}\n")
else:
    print("No potential prospects found.")