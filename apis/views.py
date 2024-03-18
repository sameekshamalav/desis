from django.shortcuts import render, redirect
from .models import Expense, UserStatus
from django.http import HttpResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt

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
@csrf_exempt
def add(request):
    if request.method == 'POST':
        item = request.POST['item']
        amount = int(request.POST['amount'])
        category = request.POST['category']
        date = request.POST['date']

        expense = Expense(item=item, amount=amount, category=category, date=date)
        expense.save()

        # Update total_expenses for the user
        user_status = UserStatus.objects.get(user_id=1)  # Assuming user_id 1 is the only user
        user_status.total_expenses += amount
        user_status.save()

    return redirect(home)

def add_user_status(request):
    if request.method == "POST":
        allowedexpense = int(request.POST.get("allowedexpense"))
        monthlybudget = int(request.POST.get("monthlybudget"))
        pincode = int(request.POST.get("pincode"))
        
        # Create or update UserStatus for the user
        user_status, created = UserStatus.objects.get_or_create(user_id=1)  # Assuming user_id 1 is the only user
        
        user_status.allowedexpense = allowedexpense
        user_status.monthlybudget = monthlybudget
        user_status.pincode = pincode
        user_status.save()
        
    return redirect(expense_summary)  # Render the form to add user status
    
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
    user_status = UserStatus.objects.get(user_id=1)

    context = {
        'category_percentages': category_percentages,
        'daily_spending_data': daily_spending_data,
        'user_status': user_status
    }
    return render(request, 'expense_summary.html', context)

    