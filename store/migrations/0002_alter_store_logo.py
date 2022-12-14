# Generated by Django 4.1 on 2022-08-17 11:37

from django.db import migrations, models
import store.validator


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(null=True, upload_to='store/images', validators=[store.validator.validate_file_size]),
        ),
    ]
