from django.db import models

class Restaurantsale(models.Model):
    POS = 'POS'
    TRANSFER = 'TRANSFER'
    CASH = 'CASH'
    DEBT = 'DEBT'
    COMPLIMENTARY = 'COMPLIMENTARY'

    MODE_OF_PAYMENT_CHOICES = [
        ('POS', 'POS'),
        ('TRANSFER', 'TRANSFER'),
        ('CASH', 'CASH'),
        ('DEBT', 'DEBT'),
        ('COMPLIMENTARY', 'COMPLIMENTARY')
    ]
    date = models.DateField()
    description = models.CharField(max_length=200)
    number_of_plates = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=MODE_OF_PAYMENT_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.number_of_plates * self.price

class Restaurantdebt(models.Model):
    sale = models.ForeignKey(Restaurantsale, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)
