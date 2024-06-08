from django.db import models

class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=255)
    # price: "$199",
    # discount: "$112",
    # offer: "70% OFF",
    # brand: "OLG",
    # // color: false,
    # // hascolor: false
