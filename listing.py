class Listing:
    def __init__(self, address, price, property_type, num_bedrooms, num_bathrooms):
        self.address = address
        self.price = self.format_price(price)
        self.property_type = property_type
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms

    def format_price(self, price):
        new_price_string = "".join([char for char in price if char.isdigit()])
        return int(new_price_string) if new_price_string else None    