from django.shortcuts import render, redirect
from .models import Expense
from django.http import HttpResponse
from django.db.models import Sum

# Create your views here.
# home
def home(request):
    expenses = Expense.objects.all()
    if request.POST:
        month = request.POST['month']
        year = request.POST['year']
        expenses = Expense.objects.filter(date__year=year, date__month=month)
    return render(request, 'index.html', {'expenses': expenses})

# create
def add(request):
    if request.method == 'POST':
        item = request.POST['item']
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']

        expense = Expense(item=item, amount=amount, category=category, date=date)
        expense.save()

    return redirect(home)

def update(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    if request.method == 'POST':
        item = request.POST['item']
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']

        expense_fetched.item = item
        expense_fetched.amount = amount
        expense_fetched.category = category
        expense_fetched.date = date

        expense_fetched.save()

    return redirect(home)

def delete(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    expense_fetched.delete()
    return redirect(home)

def expense_summary(request):
    # Retrieve all expenses from the database
    expenses = Expense.objects.all()

    # Calculate total spending for each category
    category_totals = expenses.values('category').annotate(total=Sum('amount'))

    # Calculate total spending across all categories
    total_spending = expenses.aggregate(total=Sum('amount'))['total']

    # Calculate percentage spending for each category
    category_percentages = {}
    for category_total in category_totals:
        category_percentages[category_total['category']] = (category_total['total'] / total_spending) * 100
    
    # Aggregate spending data based on dates
    daily_spending_data = expenses.values('date').annotate(total=Sum('amount'))

    context = {
        'category_percentages': category_percentages,
        'daily_spending_data': daily_spending_data
    }
    return render(request, 'expense_summary.html', context)

    