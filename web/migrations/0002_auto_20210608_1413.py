# Generated by Django 3.1.7 on 2021-06-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='storprof',
            field=models.CharField(choices=[('Student', 'Student'), ('Professional', 'Professional'), ('Other', 'Other')], default='Other', max_length=12),
        ),
    ]
