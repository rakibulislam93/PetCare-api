# Generated by Django 5.0.6 on 2024-09-20 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='petmodel',
            name='aded_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='petmodel',
            name='age',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
