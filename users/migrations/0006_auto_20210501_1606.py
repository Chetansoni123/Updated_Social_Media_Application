# Generated by Django 3.1.7 on 2021-05-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_delete_countfriends'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobile',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Mobile',
        ),
    ]
