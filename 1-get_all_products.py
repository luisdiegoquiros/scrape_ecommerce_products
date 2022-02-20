import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Run headless browser
options = Options()
options.add_argument('--headless')

# Loads the Chrome driver
s = Service('ext/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)

# Loads JSON with the URL
with open('data/categories.json', 'r') as file:
    data = json.load(file)

# Get products in each subcategory
for subcategory in data:

    print(f'Starting with category ID: {subcategory["id"]}')

    # Gets the url
    driver.get(subcategory['subcategory_link'])
    time.sleep(1)  # waits
    # scrolls to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)  # waits

    # finds the containers with each product
    products = driver.find_elements(By.CSS_SELECTOR, 'div.organic-offer-wrapper')

    results = []

    # finds all the products and saves the data
    for p in products:
        # if a product doesnt have one of the fields, skips it
        try:
            product_name = p.find_element(By.CSS_SELECTOR, 'p.elements-title-normal__content').text
            product_price = p.find_element(By.CSS_SELECTOR, 'span.elements-offer-price-normal__promotion').text
            product_country = p.find_element(By.CSS_SELECTOR, 'span.seller-tag__country').get_attribute('title')
            product_information = {
                'subcategory_id': subcategory["id"],
                'name': product_name,
                'price': float(product_price.replace('$', '')),
                'country': product_country
            }
            results.append(product_information)
        except:
            pass

# Writes the information on a json file
with open('data/products.json', 'w') as fp:
    json.dump(results, fp, indent=4)

driver.close()
