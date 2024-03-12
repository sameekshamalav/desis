from django.contrib import admin
from .models import Pincode, User, Site, Category, Product, PP, Expenses, UserStatus, Leaderboard

# Register your models here.
admin.site.register(Pincode)
admin.site.register(User)
admin.site.register(Site)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(PP)
admin.site.register(Expenses)
admin.site.register(UserStatus)
admin.site.register(Leaderboard)
