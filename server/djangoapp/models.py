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


# <HINT> Create a plain Python class `DealerReview` to hold review data
