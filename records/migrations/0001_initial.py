# Generated by Django 5.2 on 2025-05-07 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(editable=False, max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, editable=False, max_digits=15, verbose_name='Total amount in this month')),
            ],
        ),
        migrations.CreateModel(
            name='YearlyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(editable=False, max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, editable=False, max_digits=15, verbose_name='Total amount in this year')),
            ],
        ),
        migrations.CreateModel(
            name='DailyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(editable=False, max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, editable=False, max_digits=15, verbose_name='Total amount in this day')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_records', to='records.monthlyrecord', verbose_name='Month of this day')),
            ],
        ),
        migrations.AddField(
            model_name='monthlyrecord',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_records', to='records.yearlyrecord', verbose_name='Year of this day'),
        ),
    ]
