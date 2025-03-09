from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class Car:
    def __init__(self, model_type, price, description, range):
        self.model_type = model_type
        self.price = price
        self.description = description
        self.range = range
    
    def __str__(self):
        return (f"Model Type: {self.model_type}\nPrice: {self.price}\n"f"Description: {self.description}\nRange: {self.range}")

def initialize_chrome_webdriver():
    print("Initializing Chrome WebDriver...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument("--headless")
    service = ChromeService(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=chrome_options)

driver = initialize_chrome_webdriver()
driver.get("https://www.tesla.com/inventory/used/m3?PAINT=BLACK,GREY,RED&INTERIOR=PREMIUM_BLACK&VehicleHistory=CLEAN&Year=2022,2023,2024&arrangeby=distance&zip=33178&range=0")

wait = WebDriverWait(driver, 10)
results_container = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "div.results-container.results-container--grid.results-container--has-results")
))

results = results_container.find_elements(By.CSS_SELECTOR, "article.result.card")
cars = []

for result in results:
    try:
        button = result.find_element(By.TAG_NAME, "button")
        article = button.find_element(By.TAG_NAME, "article")
        card_info = article.find_element(By.CLASS_NAME, "card-info")
        section = card_info.find_element(By.TAG_NAME, "section")

        # Extract car information from the section tag
        model_type = section.find_element(By.CLASS_NAME, "tds-text--h4").text
        price = section.find_element(By.XPATH, ".//div/span/span").text
        description = section.find_element(By.CLASS_NAME, "tds-text--contrast-low").text
        range = section.find_elements(By.CLASS_NAME, "tds-text--contrast-low")[1].text

        car = Car(model_type=model_type, price=price, description=description, range=range)
        cars.append(car)
    except Exception as e:
        print(f"Skipping false result...")

driver.quit()

potential_prospects = []

for i, car in enumerate(cars):
    print(f"Result {i + 1}:\n{car}\n")

    try:    
        parsed_price = int(car.price.replace("$", "").replace(",", ""))
    except Exception as e:
        print(f"Could not parse the price of the car.")

    if parsed_price <= 25000:
        print("Found a potential prospect")
        potential_prospects.append(car)

if potential_prospects:
    for i, car in enumerate(potential_prospects):
        print(f"Potential prospect {i}:\n{car}")
else:
    print("No potential prospects found.")