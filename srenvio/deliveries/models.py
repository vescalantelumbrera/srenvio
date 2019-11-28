from django.db import models

# Create your models here.


class Delivery(models.Model):

    tracking_number = models.CharField(
        max_length=20, default="", null=False, unique=True)

    carrier = models.CharField(null=False, max_length=20)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "delivery"


class Parcel(models.Model):

    length = models.DecimalField(null=False, decimal_places=4, max_digits=9)

    width = models.DecimalField(null=False, decimal_places=4, max_digits=9)

    height = models.DecimalField(null=False, decimal_places=4, max_digits=9)

    weight = models.DecimalField(null=False, decimal_places=4, max_digits=9)

    real_length = models.DecimalField(
        null=False, decimal_places=4, max_digits=9)

    real_width = models.DecimalField(
        null=False, decimal_places=4, max_digits=9)

    real_height = models.DecimalField(
        null=False, decimal_places=4, max_digits=9)

    real_weight = models.DecimalField(
        null=False, decimal_places=4, max_digits=9)

    total_weight = models.DecimalField(
        null=False, decimal_places=4, max_digits=9)

    delivery = models.ForeignKey(
        "Delivery", on_delete=models.CASCADE, default=None
    )

    over_weight = models.IntegerField(null=False)

    class Meta:
        db_table = "parcel"
