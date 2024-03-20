from django.db import models

# Create your models here.
class Expense(models.Model):
    item = models.CharField(max_length = 50)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField()


class MailExpense(models.Model):
    id = models.AutoField(primary_key=True)
    # user_id = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    item = models.TextField()
    category = models.TextField()
    date_of_purchase = models.DateTimeField()
    platform = models.TextField(default="self")
    status = models.TextField()
    order_id = models.TextField()
    feedback = models.TextField()


# User key to identify for which user the expense is added
    def __str__(self):
        return self.item
    class Meta:
        db_table = 'expense'


class UserStatus(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name =models.CharField(max_length=100)
    total_expenses = models.IntegerField(default=0)
    number_of_expenses =models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    allowedexpense = models.IntegerField(default=0)
    monthlybudget = models.IntegerField(default=0)
    pincode = models.IntegerField(null=True)  # Assuming pincode can be nullable
    gmail = models.CharField(max_length = 50)
    app_password = models.CharField(max_length = 50)

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


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    email_id=models.CharField(max_length=255, default ='')
    user_id = models.ForeignKey(UserStatus, on_delete=models.CASCADE) # user_id = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject} - {self.sender}'
    class Meta:
        db_table = 'expense'



class MailExpense(models.Model):
    
    id = models.AutoField(primary_key=True)
    # user_id = models.CharField(max_length=255)
    user_id = models.ForeignKey(UserStatus, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    item = models.TextField()
    category = models.TextField()
    date_of_purchase = models.DateTimeField()
    platform = models.TextField(default="self")
    status = models.TextField()
    order_id = models.TextField()
    feedback = models.TextField()


    
# User key to identify for which user the expense is added
    def __str__(self):       return self.item

