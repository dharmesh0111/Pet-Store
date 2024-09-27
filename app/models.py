from django.db import models
from django.contrib.auth.models import User
#signals
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

# Create your models here.
class pet(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=100)
    petimage = models.ImageField(upload_to='media',default=0)

class cart(models.Model):
    pid=models.ForeignKey(pet,db_column="pid", on_delete=models.CASCADE)
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

def __str__(self):
    return str(self)


class order(models.Model):
    order_id = models.IntegerField()
    pid=models.ForeignKey(pet,db_column="pid", on_delete=models.CASCADE)
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    quantity = models.IntegerField()


class demo(models.Model):
    order_id = models.IntegerField()
    pid=models.ForeignKey(pet,db_column="pid", on_delete=models.CASCADE)
    uid=models.ForeignKey(User,db_column="uid", on_delete=models.CASCADE)
    quantity = models.IntegerField()


# singlas functions
@receiver(post_save,sender = User)
def post_save_user_handler(sender,instance,created,**kwargs):
    print("within post_save handlers")
    if created:
        print('user created')
        print("send data")
    else:
        print("user updated")


