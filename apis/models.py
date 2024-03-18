from django.db import models

# Create your models here.
class Expense(models.Model):
    item = models.CharField(max_length = 50)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.item
    class Meta:
        db_table = 'expense'


class UserStatus(models.Model):
    user_id = models.IntegerField(primary_key=True)
    total_expenses = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    allowedexpense = models.IntegerField(default=0)
    monthlybudget = models.IntegerField(default=0)
    pincode = models.IntegerField(null=True)  # Assuming pincode can be nullable

    @property
    def score(self):
        if self.allowedexpense != 0:
            return round((1 - (self.total_expenses / self.allowedexpense)) * 100, 2)
        else:
            return None

    @property
    def currentbalance(self):
        return self.monthlybudget - self.total_expenses
    
    class Meta:
        db_table = 'user_status'