# Generated by Django 4.0.4 on 2022-08-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='roles',
            field=models.ManyToManyField(to='auth.group'),
        ),
        migrations.AddField(
            model_name='student',
            name='roles',
            field=models.ManyToManyField(to='auth.group'),
        ),
    ]
