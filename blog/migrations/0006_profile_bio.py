# Generated by Django 3.0 on 2020-10-23 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='hello'),
            preserve_default=False,
        ),
    ]
