class Car:
    def __init__(self, type, price, description, range):
        self.type = type
        self.price = price
        self.description = description
        self.range = range
    
    def __str__(self):
        return (f"Type: {self.type}\nPrice: {self.price}\n"f"Description: {self.description}\nRange: {self.range}")