import random
import string

from django.db import models


def generate_unique_code():
    length = 6
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if Order.objects.filter(code=code).count() == 0:
            break
    return code


class Order(models.Model):
    # code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    orderer_name = models.CharField(max_length=20, default="Jan")
    orderer_surname = models.CharField(max_length=20, default="Nowak")
    dryer_model = models.CharField(max_length=11, default="dryer_20_t")
    create_at = models.DateTimeField(auto_now_add=True)
    day_to_build = models.IntegerField(null=False, default=0)


class Worker(models.Model):
    lp = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, default="Jan")
    surname = models.CharField(max_length=20, default="Nowak")
    utility_1 = models.CharField(max_length=1, default="-")
    utility_2 = models.CharField(max_length=1, default="-")
    utility_3 = models.CharField(max_length=1, default="U")
