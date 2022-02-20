import json
import time
from joblib import Parallel, delayed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from joblib.externals.loky import set_loky_pickler

set_loky_pickler("dill")


def process_subcategory(subcategory):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    import time
    print(f'Starting with category ID: {subcategory["id"]}')

    # Loads the Chrome driver
    # Run headless browser
    options = Options()
    options.add_argument('--headless')
    s = Service('ext/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)

    # Gets the url
    driver.get(subcategory['subcategory_link'])
    time.sleep(1)  # waits
    # scrolls to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)  # waits

    # finds the containers with each product
    products = driver.find_elements(By.CSS_SELECTOR, 'div.organic-offer-wrapper')

    results = []
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



    # Closes the driver
    driver.close()
    return results





# Loads JSON with the URL
with open('data/categories.json', 'r') as file:
    data = json.load(file)

# Get products in each subcategory
results = Parallel(n_jobs=6)(delayed(process_subcategory)(d) for d in data)

# Writes the information on a json file
with open('data/products.json', 'w') as fp:
    json.dump(results, fp, indent=4)


