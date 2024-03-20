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
]