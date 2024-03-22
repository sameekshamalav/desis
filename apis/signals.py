# your_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apis.views import mail_expenses_view
from .models import MailExpense, Expense

@receiver(post_save, sender=MailExpense)
def create_expense_from_mailexpense(sender, instance, created, **kwargs):
    if created:
        print('added',instance.user_id)
        if (instance.amount!=0):
             
             Expense.objects.create(
                #  user_id=instance.user_id,
                 item=instance.item,
                 amount=instance.amount,
                 category=instance.category,
                 date=instance.date_of_purchase
             )
