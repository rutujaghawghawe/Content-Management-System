import requests
from bs4 import BeautifulSoup
import csv
import time

def get_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_name_elem = soup.find('span', attrs={'class': 'a-size-medium'})
    product_name = product_name_elem.get_text(strip=True) if product_name_elem else ''

    product_price_elem = soup.select_one('#priceblock_ourprice')
    product_price = product_price_elem.get_text(strip=True) if product_price_elem else ''

    rating_elem = soup.find('span', attrs={'class': 'a-icon-alt'})
    rating = rating_elem.get_text(strip=True).split()[0] if rating_elem else ''

    num_reviews_elem = soup.find('span', attrs={'class': 'a-size-base'})
    num_reviews = num_reviews_elem.get_text(strip=True).replace(',', '') if num_reviews_elem else ''

    product_description_elem = soup.find('div', attrs={'id': 'productDescription'})
    product_description = product_description_elem.get_text(strip=True) if product_description_elem else ''

    manufacturer_elem = soup.find('a', attrs={'id': 'bylineInfo'})
    manufacturer = manufacturer_elem.get_text(strip=True) if manufacturer_elem else ''

    asin_elem = soup.find('th', string='ASIN')
    asin = asin_elem.find_next('td').get_text(strip=True) if asin_elem else ''

    return {
        'Product Name': product_name,
        'Product Price': product_price,
        'Rating': rating,
        'Number of Reviews': num_reviews,
        'Product Description': product_description,
        'Manufacturer': manufacturer,
        'ASIN': asin
    }

def scrape_products():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

    with open('product_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
                      'Product Description', 'Manufacturer', 'ASIN']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for page_num in range(1, 21):
            url = base_url.format(page_num)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all('a', attrs={'class': 'a-link-normal s-no-outline'})

            for link in product_links:
                if link.has_attr('href'):
                    product_url = 'https://www.amazon.in' + link['href']
                    product_data = get_product_details(product_url)
                    product_data['Product URL'] = product_url

                    writer.writerow(product_data)
                    csvfile.flush()  # Ensure immediate writing to the file

                    time.sleep(1)  # Delay to be respectful to the website

            print(f"Page {page_num} scraped successfully.")

scrape_products()
