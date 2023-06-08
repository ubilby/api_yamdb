# Generated by Django 3.2 on 2023-06-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_myuser_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.CharField(choices=[(0, 'User'), (1, 'Moderator'), (2, 'Admin')], default=0, max_length=64),
        ),
    ]
