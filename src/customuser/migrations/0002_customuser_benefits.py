# Generated by Django 5.1.3 on 2024-12-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benefit', '0004_benefitbase_remove_mealvoucher_description_and_more'),
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='benefits',
            field=models.ManyToManyField(related_name='colaboradores', to='benefit.benefitbase'),
        ),
    ]
