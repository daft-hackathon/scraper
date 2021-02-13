import requests as re
from fake_headers import Headers
from bs4 import BeautifulSoup
from listing import Listing
import json

def request_page(page_num):
    url = f"https://www.daft.ie/property-for-sale/dublin?from={page_num*20}"
    headers = Headers().generate()
    response = re.get(url, headers)
    if response.ok:
        return response
    else:
        return None

def get_listings_on_page(page_soup):
    data_json = json.loads(
        page_soup.find(
            "script",
            attrs = {"id": "__NEXT_DATA__"}
        ).contents[0]
    )
    return data_json["props"]["pageProps"]["listings"]
    
def parse_listing(listing):
    listing_data = listing["listing"]
    address = get_listing_attribute(listing_data, "title")
    price = get_listing_attribute(listing_data, "price")
    property_type = get_listing_attribute(listing_data, "propertyType")
    num_bedrooms = get_listing_attribute(listing_data, "numBedrooms")
    num_bathrooms = get_listing_attribute(listing_data, "numBathrooms")
    return Listing(
        address=address,
        price=price,
        property_type=property_type,
        num_bedrooms=num_bedrooms,
        num_bathrooms=num_bathrooms
    )

def get_listing_attribute(listing_data, attribute):
    try:
        return listing_data[attribute]
    except:
        return None

parsed_listings = []
page_num = 0
while True:
    response = request_page(page_num)
    if response is not None:
        response_soup = BeautifulSoup(response.text, "html5lib")
        listings = get_listings_on_page(response_soup)
        if len(listings) == 0 or page_num == 1:
            break
        else:
            for listing in listings:
                parsed_listings.append(parse_listing(listing))
            page_num += 1
    else:
        print("An unexpected error has occured")
        break

print([listing.__dict__ for listing in parsed_listings])