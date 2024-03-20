from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'index'),
    path('add', views.add, name = 'add'),
    path('update/<int:id>', views.update, name = 'update'),
    path('delete/<int:id>', views.delete, name = 'delete'),
    path('summary', views.expense_summary, name = 'summary'),
    path('add_user_status', views.add_user_status, name = 'add_user_status'),
    path('chatbot', views.chatbot_view, name = 'chatbot')
    path('process-emails/', views.process_emails_view, name='process_emails'),
    # path('process_emails/', views.process_emails_view, name='process_emails'),
    path('mail_expenses/', views.mail_expenses_view, name='mail_expenses'),
]