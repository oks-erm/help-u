# Generated by Django 4.1.1 on 2023-06-28 12:52

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userpic',
            field=cloudinary.models.CloudinaryField(default='c_scale,w_233/static/assets/img/placeholder.png', max_length=255, verbose_name='image'),
        ),
    ]
