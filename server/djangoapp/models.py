from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):

    Name = models.TextField()
    Description = models.TextField()

    def __str__(self) -> str:
        return f"{self.Name}"

    def __repr__(self) -> str:
        return f"CarMake(Name={self.Name}, Description={self.Description})"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

    Make = models.ForeignKey(CarMake, on_delete=models.DO_NOTHING)
    DealerId = models.IntegerField()
    Type = models.CharField(choices=[
            ("Sedan", "Sedan"),
            ("SUV", "SUV"), 
            ("Wagon", "Wagon"), 
            ("Hatchback", "Hatchback"),
        ], 
        max_length=50)
    Year = models.DateField()

    def __repr__(self) -> str:
        return f"CarModel(Make={self.Make}, DealerId={self.DealerId}, Type={self.Type}, Year={self.Year})"    

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, id, full_name, short_name, address, city, st, zip, lat, long):
        
        # Dealer id
        self.id = id
        # Dealer Full Name
        self.full_name = full_name
        # Dealer short name
        self.short_name = short_name

        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

        # Location lat
        self.lat = lat
        # Location long
        self.long = long

    def __str__(self):
        return f"Dealer name: {self.full_name!r}"

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, id, name, review, dealer_id, car_make, car_model, car_year, did_purchase, purchase_date):
        
        # Review id
        self.id = id
        # Customer name
        self.name = name
        # Review text / message
        self.review = review
        # Dealership
        self.dealer_id = dealer_id
        
        self.car_make = car_make

        self.car_model = car_model

        self.car_year = car_year

        self.did_purchase = did_purchase

        self.purchase_date = purchase_date


    def __str__(self):
        return f"'{self.review}' - {self.name}"