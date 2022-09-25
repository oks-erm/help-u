# Generated by Django 4.1.1 on 2022-09-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_post_city_alter_post_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Items', 'Items'), ('Services', 'Services'), ('Support', 'Support')], max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('Receive', 'Receive'), ('Give', 'Give')], max_length=10),
        ),
    ]