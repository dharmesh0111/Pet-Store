
from django.urls import path # type: ignore
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path("details/<rid>",views.details),
    path("register/",views.registration),
    path('login',views.userlogin),
    path('logout',views.userlogout),
    path('addtocart/<petid>',views.addtocart),
    path('showcart',views.showusercart),
    path('removepet/<cid>',views.removepet),
    path('updatecart/<opr>/<cartid>',views.updatecart),
    path('search/<pet_type>',views.searchbytype),
    path('range',views.pricerange),
    path('sort/<ord>',views.sortrange),
    path('placeorder',views.confirmorder),
    path('makepayment',views.makepayment),
    path('confirmpayment',views.confirmpayment),
    path('address',views.useraddress),

#  app urls

    path('expensive-pets/', views.exp_pets, name='expensive_pets'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
