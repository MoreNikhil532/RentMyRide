from django.db import models

# Create your models here.
class Vehicles(models.Model):
    reg_no = models.CharField(max_length=10,unique=True)
    city = models.CharField(max_length=20)
    v_type = models.CharField(max_length=12)
    isBooked = models.BooleanField(default = False)
    RegDate = models.DateTimeField(auto_now_add=True)
    DriverName = models.CharField(max_length=50)
    DriverContact = models.CharField(max_length=10)

    def __str__(self):
        return self.reg_no

class Dashboard(models.Model):
    u_name = models.CharField(max_length=50,unique=False)
    fromDate = models.DateField()
    toDate = models.DateField()
    cost = models.IntegerField()
    v_type = models.CharField(max_length=12)
    # isPaid = models.BooleanField(default=False)
    v_no = models.CharField( max_length=10)
    DriverName = models.CharField(max_length=50)
    DriverContact = models.CharField(max_length=10)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.u_name
    