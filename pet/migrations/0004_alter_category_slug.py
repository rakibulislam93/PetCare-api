# Generated by Django 5.0.6 on 2024-10-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0003_remove_petmodel_aded_by_petmodel_added_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]