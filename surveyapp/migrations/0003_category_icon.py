# Generated by Django 3.2 on 2021-04-06 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveyapp', '0002_rename_categories_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(max_length=15, null=True),
        ),
    ]