# Generated by Django 5.0.6 on 2024-08-13 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.png', upload_to='catimages'),
        ),
    ]
