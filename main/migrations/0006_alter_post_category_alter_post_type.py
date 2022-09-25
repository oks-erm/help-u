# Generated by Django 4.1.1 on 2022-09-23 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_post_category_alter_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('items', 'Items'), ('services', 'Services'), ('support', 'Support')], max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('receive', 'Receive'), ('give', 'Give')], max_length=10),
        ),
    ]