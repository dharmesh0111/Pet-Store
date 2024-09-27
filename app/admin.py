from django.contrib import admin
from app.models import pet,cart

# Register your models here.
class petadmin(admin.ModelAdmin):
    list_display =['id','name','type','breed','gender','age','price','description','petimage']
    list_filter = ['type','breed','price']

admin.site.register(pet,petadmin)

class cartadmin(admin.ModelAdmin):
    list_display=['id','pid','uid','quantity']

admin.site.register(cart,cartadmin)