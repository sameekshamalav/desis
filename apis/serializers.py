from rest_framework import serializers
from .models import Pincode, User, Site, Category, Product, PP, Expenses, UserStatus, Leaderboard

class PincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pincode
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PP
        fields = '__all__'

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = '__all__'
