from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Expenses
from .serializers import UserSerializer, ExpensesSerializer

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_expenses(request):
    expenses = Expenses.objects.all()
    serializer = ExpensesSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_expense(request):
    serializer = ExpensesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_expense(request, pk):
    expense = get_object_or_404(Expenses, pk=pk)
    serializer = ExpensesSerializer(expense)
    return Response(serializer.data)

@api_view(['PUT'])
def update_expense(request, pk):
    expense = get_object_or_404(Expenses, pk=pk)
    serializer = ExpensesSerializer(expense, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)