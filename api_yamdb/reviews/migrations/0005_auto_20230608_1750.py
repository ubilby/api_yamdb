# Generated by Django 3.2 on 2023-06-08 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_myuser_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'ordering': ('username',), 'verbose_name': 'Юзверь', 'verbose_name_plural': 'Юзвери'},
        ),
        migrations.AddConstraint(
            model_name='myuser',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, username='me'), name='name_not_me'),
        ),
    ]
