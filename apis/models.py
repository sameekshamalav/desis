from django.db import models
from django.core import validators
from django.utils import timezone

class Pincode(models.Model):
    pincode = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.pincode}: {self.city_name}, {self.state_name}"

    class Meta:
        db_table = 'pincode'

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=10, validators=[validators.MinLengthValidator(10)])
    email = models.EmailField()
    pincode_id = models.IntegerField()
    monthly_budget = models.IntegerField()  # Modified to snake_case
    target_savings = models.IntegerField()  # Modified to snake_case
    allowed_expense = models.IntegerField()  # Modified to snake_case
    password = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.user_id}: {self.name}"

    class Meta:
        db_table = 'user'

class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    payment_url = models.CharField(max_length=255)  # Modified to snake_case

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'site'

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'

class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'

class PP(models.Model):
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.p_id} - {self.site_id}"

    class Meta:
        db_table = 'pp'

class Expenses(models.Model):
    sno = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Product, on_delete=models.CASCADE)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sno}: {self.amount} - {self.user_id} - {self.category} - {self.site_id}"

    class Meta:
        db_table = 'expenses'

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Modified to OneToOneField
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(default=timezone.now)
    allowed_expense = models.IntegerField()  # Modified to snake_case
    monthly_budget = models.IntegerField()  # Modified to snake_case
    score = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.IntegerField()  # Modified to snake_case
    pincode = models.IntegerField()

    def __str__(self):
        return f"{self.user_id}: {self.total_expenses} - {self.score}"

    class Meta:
        db_table = 'user_status'

class Leaderboard(models.Model):
    leaderboard_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Modified to ForeignKey
    user_score = models.DecimalField(max_digits=10, decimal_places=2)
    pincode = models.IntegerField()

    def __str__(self):
        return f"{self.leaderboard_id}: {self.user} - {self.user_score}"

    class Meta:
        db_table = 'leaderboard'
