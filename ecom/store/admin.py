from django.contrib import admin
from .models import Cat, Prod, Order
# Register your models here.
admin.site.register(Cat)
admin.site.register(Prod)
admin.site.register(Order)