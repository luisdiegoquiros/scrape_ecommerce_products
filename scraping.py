import json
import bs4
import requests


def get_data(url, headers) -> bs4.BeautifulSoup:
    """
    Gets data from a url using the provided headers

    :param url: webpage to get the data from
    :param headers: header to use for the get request
    :return: BeautifulSoup object with the data
    """
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    return soup


def get_categories(soup: bs4.BeautifulSoup):
    """
    From a URL gets the departments, categories and subcategories.
    :param soup: BeautifulSoup object with the data from the webpage
    :return: Pandas DataFrame with the information
    """
    # List of dictionaries to storage the data
    list_information = []

    # get the department container
    department_divs = soup.find_all('div', {'class': 'item util-clearfix'})

    # process department container
    for department in department_divs:
        department_name = department.find('h3', {'class': 'big-title'})
        department_name = department_name.text.strip()
        # process category container
        for category in department.find_all('div', {'class': 'sub-item'}):
            category_h4 = category.find('h4', {'class': 'sub-title'})
            links = category_h4.find('a', href=True)
            category_link = links['href']
            category_name = links.text.strip()
            # process subcategory container
            for subcategory in category.find_all('li'):
                links = subcategory.find('a', href=True)
                subcategory_link = links['href']
                subcategory_name = links.text.strip()
                # create dictionary with the data
                information = {
                    'department': department_name,
                    'category': category_name,
                    'category': category_name,
                    'category_link': category_link,
                    'subcategory': subcategory_name,
                    'subcategory_link': subcategory_link
                }
                # append dictionary to the list
                list_information.append(information)

    # returns list of dictionaries with the data
    return list_information


# URL with all the categories
url = 'https://www.alibaba.com/Products'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
}

soup = get_data(url, headers)
all_subcategories = get_categories(soup)

# Writes the information on a json file
with open('data/categories.json', 'w') as fp:
    json.dump(all_subcategories, fp, indent=4)
