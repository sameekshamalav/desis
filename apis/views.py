from email.utils import parsedate_to_datetime
import genericpath
import random
from types import GenericAlias
from django.http import HttpResponse
from django.shortcuts import render, redirect
from grpc import GenericRpcHandler
from numpy import generic
from .models import Expense, UserStatus,Email,MailExpense,User
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from openai import ChatCompletion
import openai,requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import imaplib
import email
import re
import google.generativeai as genai
from datetime import datetime, timedelta
import json
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

# from rest_framework import status
# from rest_framework.generics import CreateAPIView, RetrieveAPIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from .serializers import UserRegistrationSerializer
# from .serializers import UserLoginSerializer, UserDetailSerializer
# from .models import UserProfile

 # Updated import
# from .tasks import process_emails

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
from .models import User
from django.shortcuts import render
from .serializers import MailExpenseSerializer, UserSerializer,User
from django.http import JsonResponse
from .utils import generate_jwt_token
import jwt
from .models import User
from .forms import UserForm

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class MailExpenseListCreateView(generics.ListCreateAPIView):
    queryset = MailExpense.objects.all()
    serializer_class = MailExpenseSerializer

class MailExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MailExpense.objects.all()
    serializer_class = MailExpenseSerializer


def get_user_credentials(request, user_id):
    try:
        email, app_password = User.get_user_credentials(user_id)
        if email and app_password:
            return JsonResponse({'email': email, 'app_password': app_password})
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')  # Redirect to a success page
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def generate_token(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        token = generate_jwt_token(user)
        return JsonResponse({'token': token})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)

def decode_token(request):
    token = request.GET.get('token')
    if token:
        try:
            decoded_message = jwt.decode(token)
            return JsonResponse(decoded_message)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Token not provided'}, status=400)


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
        # gmail=str(request.POST.get("gmail"))
        # app_password=str(request.POST.get("a"))
        # Create or update UserStatus for the user
        user_status, created = UserStatus.objects.get_or_create(user_status=request.user_status) 
        user_status.allowedexpense = allowedexpense
        user_status.monthlybudget = monthlybudget
        user_status.pincode = pincode
        # user_status.gmail = gmail
        # user_status.app_password = app_password 
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
    user_id = request.user_id
    expenses = Expense.objects.all()

    # Calculate total spending for each category
    category_totals = expenses.values('category').annotate(total=Sum('amount'))

    # Calculate total spending across all categories
    total_spending = expenses.aggregate(total=Sum('amount'))['total']

    # Calculate percentage spending for each category
    category_percentages = {}
    for category_total in category_totals:
        category_percentages[category_total['category']] = (category_total['total'] / total_spending) * 100
    user_id=User.objects.get(user_id)
    # Aggregate spending data based on dates
    daily_spending_data = expenses.values('date').annotate(total=Sum('amount'))
    user_status = UserStatus.objects.get(user_id)
    print(user_id,"qwerru")
    context = {
        'category_percentages': category_percentages,
        'daily_spending_data': daily_spending_data,
        'user_status': user_status
    }
    return render(request, 'expense_summary.html', context)

def process_emails(username,password,user):
    print(user)
   
    # Function to connect to the IMAP server
    def connect_to_imap(username, password):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username, password)
        return mail

    # Function to fetch emails from the inbox within the last 2 minutes
    def fetch_emails_within_last_two_minutes(mail):
        two_minutes_ago = datetime.now() - timedelta(days=1)
        date_two_minutes_ago = two_minutes_ago.strftime('%d-%b-%Y')
        mail.select('inbox')
        _, data = mail.search(None, f'(SINCE "{date_two_minutes_ago}")')
        email_ids = data[0].split()
        emails = []
        for email_id in email_ids:
            _, data = mail.fetch(email_id, '(RFC822)')
            emails.append((email_id, data[0][1]))
        return emails

    # Function to parse email content and extract relevant information
    def parse_email(email_content):
        msg = email.message_from_bytes(email_content)
        sender = msg['From']
        subject = msg['Subject']
        body = ""
        # received_at = parsedate_to_datetime(msg['Date'])

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        return {"sender": sender, "subject": subject, "body": body}

    # Function to identify order-related emails using regular expressions
    def identify_order_emails(emails):
        order_emails = []
        for email_id, email_content in emails:
            try:
                con = parse_email(email_content)
                if re.search(r'(order\s+(summary|confirmation)|order\s+placed)', con["subject"], re.IGNORECASE) or re.search(r'(order\s+(summary|confirmation)|order\s+placed)', con["body"], re.IGNORECASE):
                    order_emails.append((email_id, con))
            except:
                pass
        return order_emails

    def string_to_dict(string_data):
        string_data=string_data.strip('```')
        string_data.replace('```python\n', '')


    # Fixing the string (adding commas and quotes)
        fixed_string = string_data.replace("\n", ",\n")
        fixed_string = fixed_string.replace("{", "{\"")
        fixed_string = fixed_string.replace("}", "\"}")
        fixed_string = fixed_string.replace(":", "\":\"")
        fixed_string = fixed_string.replace(",\"", ",\"")
        fixed_string = fixed_string.replace(",\n\"", ",\n\"")

        # Remove ``` at the beginning and end
        fixed_string = fixed_string.strip("```")
        fixed_string.strip()
        
        fixed_string = fixed_string.split(" = ")
        fixed_string = fixed_string[0] if len(fixed_string) == 1 else fixed_string[1]
        fixed_string.strip()
        fixed_string = fixed_string.replace(r'{",','{')
        fixed_string = fixed_string.replace(r'"},','}')
        print("fs: ",fixed_string)
        print(type(fixed_string))
        data_string = fixed_string.replace('":', '":')

# Split the string by commas
        key_value_pairs = data_string.split(',')

        # Initialize an empty dictionary
        data_dict = {}

        # Iterate through each key-value pair
        for pair in key_value_pairs:
            print(pair)
            # Split the pair into key and value
            try:
                arr  = pair.split('":"')
                key =arr[0]
                if len(arr)>2:
                    value = ":".join(arr[1:])
                else:
                    value = arr[1]
                # Remove extra double quotes
                key = key.strip().strip('"').lower()
                value = value.strip().strip('"')
                if key == 'date/time':
                    value = value.split('.')[0]
                # Add key-value pair to dictionary
                data_dict[key] = value
            except:
                pass


     
        # Convert string to dictionary
        print(data_dict)
        return data_dict
    # Function to store emails in the Django model Email
    def store_emails_in_db(emails,user=user):
        for email_id, email_data in emails:
            Email.objects.create(
                email_id=email_id,  # Save email_id to identify emails uniquely
                user_id=User.objects.filter(pk=user).first(),
                sender=email_data["sender"],
                subject=email_data["subject"],
                body=email_data["body"],
                # received_at=email_data["received_at"]
                received_at=datetime.now()
            )

    # Function to process emails using Gemini
    def process_emails_with_gemini(user=user):
        # Configure Gemini connection (replace with your API key)
        genai.configure(api_key="AIzaSyCvKJkmaRe-mSDEiz-biZS-xT2jkjGY9RU")
        model = genai.GenerativeModel('gemini-pro')
        query_set = list(Email.objects.filter(processed=False,user_id=user).all())        
        print(query_set)
        for email_data in query_set :  # Only process emails not marked as processed
          
            gemini_prompt = f'''
                the Gemini will give me the user_id (same as given above) ,
                Sender_platform (the ecommerce platform name from where the order has been place: can be decoded by the senders email) ,
                sender_icon (a code to decode the e-commerce platform from the sender email and then in the table insert their respective icon) ,
                order_id ( any id/number that is given in the email as an order id) ,
                the product name ( identity the name of the product from the mail body if not identified any then save as ITEM) ,
                category ( try to classify the type of product as in a category , like electronics ,clothes ,homeware etc, If the product name is ITEM or not able to classify the product then save as OTHER) ,
                amount ( identify the total amount of the order from the email body, generally the max amount followed by the symbol Rs. ) ,
                date/time ( date/time of the order placed) ,
                status ( whether the order is confirmed, delivered, returned, also if the Gemini finds a email with same email order, then without adding a new row, only update this status )  ,
                feedback ( if there is a link in the body asking the user to give the feedback , then upload that link in this column , if nothing is given then keep it empty, return it in python dictionary format )
                '''+f"{email_data.email_id},{email_data.user_id},{email_data.sender},{email_data.subject},{email_data.body},{email_data.received_at}"

            response = model.generate_content(gemini_prompt)
            order_info = response.text.split("|")
           
            orde_dic = string_to_dict(order_info[0])
    # Fixing the string (adding commas and quotes
            print("od",orde_dic)
            keys = list(orde_dic.keys())
            print(keys)
            
            sender_platform = email_data.sender.split("@")[1].split(".")[0]
            user_id = email_data.user_id 
            order_id = orde_dic["order_id"] if "order_id" in keys else "_"
            product_name = orde_dic["product_name"] if "product_name" in keys else "_"
            category = orde_dic["category"] if "category" in keys else "_"
            # Handle potential conversion errors for amount
            amount = 0  # Default value if conversion fails
            if "amount" in keys and orde_dic["amount"] is not None:
                try:
                        amount = int(orde_dic["amount"])
                except ValueError:
        # Handle the case where orde_dic["amount"] is not a valid integer
        # For example, you could log an error message or take another appropriate action
                            pass

            # amount = int(orde_dic["amount"] if "amount" in keys and orde_dic["amount"] is not None else '0')
            # amount = int(orde_dic.get("amount", 0))
            # date_time_format = '%A %B %d %Y at %H":"%M'
            # date_time_format = '%Y-%m-%d %H:%M:%S.%f%z'    
            # date_time = datetime.strptime(orde_dic["date/time"],date_time_format) 
            # if "date/time" in keys else datetime.now()
            # date_time=date_time.strftime(r'%Y-%m-%d %H:%M:%S')
            if '.' in orde_dic["date/time"] and '+' in orde_dic["date/time"]:
                date_time_format = '%Y-%m-%d %H:%M:%S.%f%z'
            else:
                date_time_format = '%Y-%m-%d %H:%M:%S'

# Parse the string to datetime object
            try:
                date_time = datetime.strptime(orde_dic["date/time"], date_time_format)    
            except ValueError:
                    print("Error: Provided date/time string does not match the expected format.")      
            status = orde_dic["status"] if "status" in keys else "_"
            feedback = orde_dic["feedback"] if "feedback" in keys else "_"
             
            

            # Store data in MailExpense model
            MailExpense.objects.create(
                user_id=User.objects.filter(pk=user).first(),
                platform=sender_platform,
                order_id=order_id,
                item=product_name,
                category=category,
                amount=amount,
                date_of_purchase=date_time,
                status=status,
                feedback=feedback
            )

            # Mark email as processed
            email_data.processed = True
            email_data.save()

    # Main function to process data and insert into the database

    def process_data_and_insert(username,password):
    # Fetching user credentials
        
            mail = connect_to_imap(username, password)
            emails = fetch_emails_within_last_two_minutes(mail)
            # print(emails)
            order_emails = identify_order_emails(emails)
            print(order_emails)
            store_emails_in_db(order_emails)
            process_emails_with_gemini(user)

    process_data_and_insert(username, password)
    return True
    
    
def process_emails_view(request):
    if request.method == 'POST':
        # Assuming username and password are passed in the request
        username = request.POST.get('gmail')
        password = request.POST.get('app_password')
        # request.POST.get('password')
# def process_emails_view(request):
#     if request.method == 'POST':
#         # Assuming username and password are passed in the request
#         username = request.POST.get('gmail')
#         password = request.POST.get('app_password')
#         # request.POST.get('password')

#         # Trigger the Celery task
#         process_emails.delay(username, password)

#         return JsonResponse({'message': 'Email processing started successfully.'},status=200)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed.'}, status=400)


@api_view(["POST",])
# def mail_expenses_view(request):
#     data = request.data
#     # email = data["email"]
#     user_id = data["id"]
#     # Check if the user exists based on the provided email
#     try:
#         # user = User.objects.get(gmail=email)
#         user = User.objects.get(user_id=user_id)
#     except User.DoesNotExist:
#         return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     # Obtain the user_id directly from the user object
#     user_id = user.pk
#     print(user_id)
#     apppassword = User.objects.get(user_id=user_id).app_password
#     gmail= User.objects.get(user_id=user_id).gmail
#     # password = data["password"]
#     process = process_emails(gmail, apppassword, user_id)
    
#     # Assuming process_emails function returns a boolean indicating success or failure
#     if process:
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
#         return Response({"message": "Failed to process emails"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def mail_expenses_view(request):
    data = request.data
    
    # Ensure that 'id' is present in the request data
    if 'id' not in data:
        return Response({"message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = data["id"]
    
    try:
        # Check if the user exists based on the provided user_id
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Retrieve user's email and app_password
    gmail = user.gmail
    print(gmail,"x")
    apppassword = user.app_password
    
    # Call process_emails function
    process = process_emails(gmail, apppassword, user_id)
    
    # Assuming process_emails function returns a boolean indicating success or failure
    if process:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"message": "Failed to process emails"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_user(request):
    # Generate a random 4-digit user_id
    user_id = random.randint(1000, 9999)
    # Ensure user_id doesn't already exist
    while User.objects.filter(user_id=user_id).exists():
        user_id = random.randint(1000, 9999)
    
    # Other user data
    user_name = "Sample User"  # You can replace this with actual user data
    phone_number = "1234567890"  # You can replace this with actual user data
    gmail = "example@example.com"  # You can replace this with actual user data
    login_password = "password"  # You can replace this with actual user data
    app_password = "app_password"  # You can replace this with actual user data

    # Create the user
    user = User.objects.create(
        user_id=user_id,
        user_name=user_name,
        phone_number=phone_number,
        gmail=gmail,
        login_password=login_password,
        app_password=app_password
    )

    return HttpResponse(f"User created with user_id: {user_id}")



def login(request):
    if request.method == 'POST':
        gmail = request.POST.get('gmail')
        login_password = request.POST.get('login_password')
        try:
            user = User.objects.get(gmail=gmail, login_password=login_password)
            return JsonResponse({'exists': True})
        except User.DoesNotExist:
            return JsonResponse({'exists': False})
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to home page after successful signup
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return render(request, 'index.html')