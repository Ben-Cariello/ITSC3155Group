# Generated by Django 5.1.1 on 2024-12-03 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_userprofile_user_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='applied_jobs',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
