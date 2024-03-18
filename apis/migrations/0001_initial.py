# Generated by Django 5.0.3 on 2024-03-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
    ]