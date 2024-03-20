from django.shortcuts import render, redirect
from .models import Expense, UserStatus
from django.http import HttpResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from openai import ChatCompletion
import openai,requests
# Create your views here.
global conversation
info_string=""
# home
def prompt(request):
    expenses = Expense.objects.all()
    my_expense=format_expenses_as_table(expenses)
    user_status = UserStatus.objects.get(user_id=1)
    my_status=format_user_status_table(user_status)
    
    request.session['conversation']=[]
    request.session['conversation'].append({"role": "system", "content": "Hello, you are a financial bot your name is DE Shaw Bot. I am sharing you my expenditure data in the format Item |Amount|Category|Date and the amount are in Indian National Rupees and always try to retun the responses with data "+my_expense+"\nNow I am giving you my user status too to help you make more personalised responses and advices (the user status is in format attribute|value):"+my_status})

def home(request):
    conversation=request.session['conversation']
    expenses = Expense.objects.all()
    if request.POST:
        month = request.POST['month']
        year = request.POST['year']
        expenses = Expense.objects.filter(date__year=year, date__month=month)
    
    return render(request, 'index.html', {'expenses': expenses, 'conversation': conversation})

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
        prompt(request)
        # # Update total_expenses for the user
        # user_status = UserStatus.objects.get(user_id=1)  # Assuming user_id 1 is the only user
        # user_status.total_expenses += amount
        # user_status.save()

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
        prompt(request)
    return redirect(expense_summary)  # Render the form to add user status
    
def update(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    # user_status = UserStatus.objects.get(user_id=1)  # Assuming user_id 1 is the only user
    # user_status.total_expenses -= expense_fetched.amount
    
    if request.method == 'POST':
        
        item = request.POST['item']
        amount = int(request.POST['amount'])
        category = request.POST['category']
        date = request.POST['date']

        expense_fetched.item = item
        expense_fetched.amount = amount
        expense_fetched.category = category
        expense_fetched.date = date
        # user_status.total_expenses+=amount
        # user_status.save()
        expense_fetched.save()
        prompt(request)
    return redirect(home)

def delete(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    
    # user_status = UserStatus.objects.get(user_id=1)  # Assuming user_id 1 is the only user
    # user_status.total_expenses -= expense_fetched.amount
    # user_status.save()
    expense_fetched.delete()
    prompt(request)
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

def format_expenses_as_table(expenses):
    # Define headers for the table
    headers = ["Item", "Amount", "Category", "Date"]

    # Create a list to hold each row of data
    table_data = []

    # Append headers as the first row of the table
    table_data.append(headers)

    # Iterate over each expense object and append its attributes as a row in the table
    for expense in expenses:
        row = [expense.item, expense.amount, expense.category, expense.date]
        table_data.append(row)

    # Calculate the maximum width of each column
    col_widths = [max(len(str(row[i])) for row in table_data) for i in range(len(headers))]

    # Format the table
    formatted_table = ""
    for row in table_data:
        formatted_table += "|".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(headers))) + "\n"

    return formatted_table

def format_user_status_table(user_status):
    # Initialize the header and separator
    table = "Attribute            | Value\n"
    

    # Iterate over each field in the UserStatus model
    for field in user_status._meta.fields:
        # Format the field name and value
        field_name = field.name.capitalize().replace('_', ' ')
        field_value = getattr(user_status, field.name)
        
        # Add the field name and value to the table
        table += f"{field_name.ljust(20)}| {field_value}\n"

    return table

def chatbot_view(request):
    conversation=request.session['conversation']
    expenses = Expense.objects.all()
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Append user input to the conversation
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Define the API endpoint and parameters
        api_endpoint = "https://api.openai.com/v1/chat/completions"
        api_key = "ENTER YOUR KEY HERE"  # Replace with your actual API key
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": conversation
        }

        # Make a POST request to the API
        response = requests.post(api_endpoint, json=data, headers=headers)

        # Extract chatbot replies from the API response
        if response.status_code == 200:
            chatbot_replies = [message['message']['content'] for message in response.json()['choices'] if message['message']['role'] == 'assistant']
            # Append chatbot replies to the conversation
            for reply in chatbot_replies:
                conversation.append({"role": "assistant", "content": reply})

            # Update the conversation in the session
            request.session['conversation'] = conversation
            
    # Render the template with the updated conversation
    
    return render(request, 'index.html', {'conversation': request.session['conversation'], 'expenses': expenses})
