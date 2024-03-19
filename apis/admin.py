from django.contrib import admin
from .models import Expense,UserStatus

# Register your models here.
admin.site.register(Expense)
admin.site.register(UserStatus)