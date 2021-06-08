# Generated by Django 3.1.7 on 2021-06-03 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin', models.CharField(max_length=250)),
                ('about', models.CharField(max_length=500)),
                ('storprof', models.CharField(choices=[('Student', 'Student'), ('Professional', 'Professional'), ('Other', 'Other')], default='Other', max_length=12, unique=True)),
                ('where_do_you_work', models.CharField(max_length=50)),
                ('graduation_year', models.IntegerField()),
                ('blog_post', models.BooleanField(default=False)),
                ('newletter', models.BooleanField(default=False)),
                ('offers', models.BooleanField(default=False)),
                ('uname', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
